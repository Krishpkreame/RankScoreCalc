class rankscoresorter():
    def sort(self, data):
        final_dict = {}

        def orderofgrades(item):
            if item == "Achieved":
                return 3
            elif item == "Achieved with Merit":
                return 2
            elif item == "Achieved with Excellence":
                return 1
            else:
                return 4

        for x in data:
            if len(data[x]) < 2:
                final_dict.update({x: data[x]})
                continue

            sorted_stanards = sorted(
                data[x].items(),
                key=lambda x: orderofgrades(x[1][1]))

            final_dict.update({x: sorted_stanards})
        return final_dict
