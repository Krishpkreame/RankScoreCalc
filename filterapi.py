import json


class filter_kamar():
    def __init__(self, uestandards):
        self.ue_app_subs = json.loads(uestandards)

    def filter_results(self, results):
        self.results_sorted = {}
        for i_student_result in results.keys():
            for i_ue_sub in self.ue_app_subs.keys():
                if int(i_student_result) in self.ue_app_subs[i_ue_sub]:
                    if i_ue_sub in self.results_sorted.keys():
                        self.results_sorted[i_ue_sub].update({
                            "subject_credits_earned": self.results_sorted[i_ue_sub]["subject_credits_earned"] + results[i_student_result][0],
                            i_student_result: results[i_student_result]})
                    else:
                        self.results_sorted.update(
                            {i_ue_sub: {
                                "subject_credits_earned": results[i_student_result][0],
                                i_student_result: results[i_student_result]}})
        return self.results_sorted
        with open("test.json", "w") as f:  # !
            f.write(json.dumps(self.results_sorted, indent=2))
