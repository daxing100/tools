import xlwt
from xmindparser import xmind_to_dict
import argparse


class XmindToXls:
    def resolvePath(self, dict, lists, title):
        # title去除首尾空格
        title = title.strip()
        # 如果title是空字符串，则直接获取value
        if len(title) == 0:
            concatTitle = dict['title'].strip()
        else:
            concatTitle = title + '\t' + dict['title'].strip()
        if dict.__contains__('topics') is False:
            lists.append(concatTitle)
        else:
            for d in dict['topics']:
                self.resolvePath(d, lists, concatTitle)

    def xmind_cat(self, list, excelname):

        f = xlwt.Workbook()
        # 生成excel文件，单sheet，sheet名为：用例
        sheet = f.add_sheet('用例', cell_overwrite_ok=True)

        row0 = ['用例名称', '前置条件', '用例步骤', '预期结果', '是否冒烟case','优先级']

        # 生成第一行中固定表头内容
        for i in range(0, len(row0)):
            sheet.write(0, i, row0[i])

        # 增量索引
        index = 0

        for h in range(0, len(list)):
            lists = []
            self.resolvePath(list[h], lists, '')
            for j in range(0, len(lists)):
                lists[j] = lists[j].split('\t')
                # 预期结果，取得是路径上的最后一个节点
                expect_result = lists[j][-1]
                # 步骤，取得是路径上的倒数第二个节点
                steps = lists[j][-2]

                # 把步骤分割，取"，"后面的操作步骤
                try:
                    carry_step = steps.split('；', 1)[1:][0]
                except:
                    carry_step = steps
                try:
                    flyback = steps.split('；')[0]
                    if flyback == steps:
                        flyback = "否"
                    elif flyback == "冒烟":
                        flyback = "是"
                except Exception as exe:
                    flyback = "否"

                try:
                    priority = "P1"
                    if flyback == "是":
                        priority = "P0"
                except Exception as exe:
                        priority = "P1"

                pre_condition = '--'.join(lists[j][:-2])

                # 写入用例名称
                sheet.write(j + index + 1, 0, str(pre_condition) + "，" + str(carry_step) + "，" + str(expect_result))
                # 写入前置条件
                sheet.write(j + index + 1, 1, pre_condition)
                # 写入用例步骤
                sheet.write(j + index + 1, 2, carry_step)
                # 写入预期结果
                sheet.write(j + index + 1, 3, expect_result)
                # 写入是否总包case
                sheet.write(j + index + 1, 4, flyback)
                # 写入case优先级
                sheet.write(j + index + 1, 5, priority)

            if j == len(lists) - 1:
                index += len(lists)
        f.save(excelname)

    def maintest(self, filename):
        out = xmind_to_dict(filename)
        excelname = filename.split('/')[-1].split('.')[0] + '.xls'
        self.xmind_cat(out[0]['topic']['topics'], excelname)


if __name__ == '__main__':
    #filename = '/Users/hanxing/Downloads/case.xmind'
    parser = argparse.ArgumentParser(usage="usage", description="description")
    parser.add_argument('-f', '--file', dest='file', type=str, default='', help='xmind文件所在路径')
    args = parser.parse_args()
    xmind_file = args.file
    a = XmindToXls().maintest(xmind_file)
