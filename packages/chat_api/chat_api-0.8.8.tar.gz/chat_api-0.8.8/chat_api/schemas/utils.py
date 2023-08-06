from collections import defaultdict
from copy import copy
from django.utils.translation import ugettext_lazy as _
from simpleeval import simple_eval


def validate_variable_modifications(obj, errors):
    """Appends variable modifications errors to list of errors"""
    errors["variable_modifications"] = []

    if isinstance(obj.variable_modifications, list):
        for rule in obj.variable_modifications:
            if not isinstance(rule, list):
                errors["variable_modifications"].append(
                    _("%s is not a list" % rule))
            elif len(rule) != 2:
                errors["variable_modifications"].append(
                    _("[%s] is not two elements list." % ", ".join(str(r) for r in rule)))
            else:
                try:
                    compile(rule[0], "fakemodule", "eval")
                except SyntaxError:
                    errors["variable_modifications"].append(
                        _("[%s] is not valid python variable name." % rule[0]))
                try:
                    float(rule[0])
                    errors["variable_modifications"].append(
                        _("%s is not valid python variable name. Can't be number." % rule[0]))
                except ValueError:
                    pass
                try:
                    compile(rule[1], "fakemodule", "eval")
                except SyntaxError:
                    errors["variable_modifications"].append(
                        _("[%s] is not valid python expression."
                          " Please separate variables and operators with spaces." % rule[1]))

    else:
        errors["variable_modifications"].append(
            _("%s is not a list" % obj.variable_modifications))

    return errors


class SchemaChecker(object):
    MAX_VISITS_IN_ONE_NODE_WITH_DIFFERENT_SIGNATURES = 10

    def __init__(self, schema):
        self.schema = schema
        self.errors = set()
        self.visited_questions = set()
        self.visited_signatures = set()
        self.questions_map = set()
        self.answers_map = {}
        self.forking_set = set()
        self.reached_forking_set = set()

    def get_signature(self, qid, variables_pool):
        return (qid, ) + tuple(variables_pool.items())

    @classmethod
    def format_path(cls, path):
        # extract only the loop part
        last_qid = path[-1][0]
        for i in range(len(path) - 2, 0, -1):
            if path[i][0] == last_qid:
                path = path[i:]
                break
        return "Path: %s" % ", ".join(str(x[0]) for x in path)

    @classmethod
    def get_forking_params(cls, question, variables_pool):
        for qid, condition in question.forking_rules:
            if simple_eval(condition, names=variables_pool):
                return int(simple_eval(qid, names=variables_pool)), condition
        return -1, ""

    @classmethod
    def apply_variables_modifications(cls, variables_pool, variable_modifications):
        for symbol, expression in variable_modifications:
            variables_pool[symbol] = simple_eval(expression, names=variables_pool)

    def dfs(self, qid, path, variables_pool, visited_questions_counter):
        if qid == -1:
            return

        if qid not in self.questions_map:
            self.errors.add("Question with QID %d does not exists." % qid)
            return
        question = self.questions_map[qid]

        # update variables pool
        if question.variable_modifications:
            self.apply_variables_modifications(variables_pool, question.variable_modifications)

        # get signature
        signature = self.get_signature(qid, variables_pool)

        # check for loops & add to signature set and path
        if signature in self.visited_signatures:
            if signature in path:
                self.errors.add("Infinite loop detected. %s" % self.format_path(path + [(qid, )]))
            return
        path.append(signature)
        self.visited_signatures.add(signature)
        self.visited_questions.add(qid)

        # update visited questions counter & check for loops
        if qid not in visited_questions_counter:
            visited_questions_counter[qid] = 1
        else:
            visited_questions_counter[qid] += 1
        if visited_questions_counter[qid] > self.MAX_VISITS_IN_ONE_NODE_WITH_DIFFERENT_SIGNATURES:
            self.errors.add("Infinite loop detected. %s" % (self.format_path(path)))
            return

        # follow to the next question
        if question.type == question.TYPE_FORK:
            next_qid, forking_rule = self.get_forking_params(question, variables_pool)
            self.reached_forking_set.add((qid, forking_rule))
            self.dfs(next_qid, copy(path), copy(variables_pool), copy(visited_questions_counter))
        elif question.type in (question.TYPE_CHOICE, question.TYPE_MULTICHOICE):
            for answer in self.answers_map.get(qid, []):
                new_variables_pool = copy(variables_pool)
                if answer.variable_modifications:
                    self.apply_variables_modifications(new_variables_pool, answer.variable_modifications)
                self.dfs(answer.next_qid, copy(path), new_variables_pool, copy(visited_questions_counter))

            # simulate choosing all non-exclusive answers with variables modifications (if more than 1 exists)
            if question.type == question.TYPE_MULTICHOICE:
                first_answer = None
                variable_modifications_count = 0
                new_variables_pool = copy(variables_pool)
                for answer in self.answers_map.get(qid, []):
                    if not answer.exclusive and answer.variable_modifications:
                        if not first_answer:
                            first_answer = answer
                        variable_modifications_count += 1
                        self.apply_variables_modifications(new_variables_pool, answer.variable_modifications)
                if first_answer and variable_modifications_count > 1:
                    self.dfs(first_answer.next_qid, copy(path), new_variables_pool, copy(visited_questions_counter))
        else:
            self.dfs(question.next_qid, copy(path), copy(variables_pool), copy(visited_questions_counter))

    def run(self):
        from chat_api.schemas.models import Answer, Question

        self.questions_map = dict((q.qid, q) for q in Question.objects.filter(schema=self.schema))
        first_question = Question.objects.filter(schema=self.schema).order_by("position").first()

        for question in self.questions_map.values():
            if question.type == Question.TYPE_FORK:
                for rule in question.forking_rules:
                    self.forking_set.add((question.qid, rule[1]))

        for answer in Answer.objects.filter(question__schema=self.schema):
            if answer.question.qid not in self.answers_map:
                self.answers_map[answer.question.qid] = []
            self.answers_map[answer.question.qid].append(answer)

        self.dfs(first_question.qid, [], defaultdict(float, {"_______________": 0}), {})

        not_visited_questions = set(self.questions_map.keys()) - self.visited_questions - {first_question.qid}
        for qid in not_visited_questions:
            self.errors.add("No path to question with QID %d." % qid)

        for unreached_fork in self.forking_set - self.reached_forking_set:
            self.errors.add(
                "Unreachable condition \"%s\" in fork with QID %d" % (unreached_fork[1], unreached_fork[0])
            )

        self.errors = sorted(list(self.errors))
        return not bool(self.errors)
