from analysis_basic import AnalysisBasic

class Loto7Analysis(AnalysisBasic):
    def __init__(self, loto7_data):
        super().__init__(loto7_data, 7)

    def __str__(self):
        return 'ロト7の当選番号を予想します。'


if __name__ == '__main__':
    pass
