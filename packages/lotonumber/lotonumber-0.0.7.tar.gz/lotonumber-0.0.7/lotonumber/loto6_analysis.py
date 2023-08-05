from analysis_basic import AnalysisBasic

class Loto6Analysis(AnalysisBasic):
    def __init__(self, loto6_data):
        super().__init__(loto6_data, 6)

    def __str__(self):
        return 'ロト6の当選番号を予想します。'


if __name__ == '__main__':
    pass

