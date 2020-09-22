# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import os
from datetime import datetime, timedelta
from uuid import uuid1
# libraries and data
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class SysReportGenerator(object):
    def __init__(self):
        dir_tmp = os.getenv('OPBOT_FILE_DIR')

        if dir_tmp is not None:
            if not os.path.exists(dir_tmp):
                os.makedirs(dir_tmp)
            self.__save_dir = dir_tmp + "/"
        else:
            self.__save_dir = ""

    def cpu_report(self, user_id, node_list):
        """
        노드별 CPU 사용량 반환.
        :param user_id:
        :param node_list:
        :return file_name:
        """
        date_list = list()
        for i in range(0, 30):
            d = datetime.now() - timedelta(days=i)
            date_list.append(d.strftime('%m/%d'))

        data = dict()
        data["x"] = date_list

        for i, node in enumerate(node_list):
            if i == 0:
                data[node] = np.random.rand(30) * 10
            elif i == 1:
                data[node] = np.random.rand(30) * 12
            elif i == 2:
                data[node] = np.random.rand(30) * 14
            elif i == 3:
                data[node] = np.random.rand(30) * 16
            elif i == 4:
                data[node] = np.random.rand(30) * 13

        # Make a data frame
        df = pd.DataFrame(data)

        plt.clf()
        # style
        plt.style.use('seaborn-darkgrid')

        # create a color palette
        palette = plt.get_cmap('Set1')

        # multiple line plot
        num = 0
        for column in df.drop('x', axis=1):
            num += 1
            plt.plot(df['x'], df[column], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)

        # Add legend
        plt.legend(loc=2, ncol=2)

        # Add titles
        plt.title("CPU Usage({}~{})".format(date_list[-1], date_list[0]),
                  loc='left', fontsize=12, fontweight=0, color='orange')
        plt.xlabel("Date")
        plt.ylabel("CPU Usage(%)")
        plt.axis([date_list[-1], date_list[0], 0, 100])
        plt.xticks(rotation=90)
        c_name = "{}{}{}.png".format(self.__save_dir, user_id, str(uuid1()))
        plt.savefig(c_name)

        return c_name

    def mem_report(self, user_id, node_list):
        """
        노드별 Memory 사용량 반환.
        :param user_id:
        :param node_list:
        :return file_name:
        """
        date_list = list()
        for i in range(0, 30):
            d = datetime.now() - timedelta(days=i)
            date_list.append(d.strftime('%m/%d'))

        data = dict()
        data["x"] = date_list

        for i, node in enumerate(node_list):
            if i == 0:
                data[node] = np.random.rand(30) * 30
            elif i == 1:
                data[node] = np.random.rand(30) * 32
            elif i == 2:
                data[node] = np.random.rand(30) * 34
            elif i == 3:
                data[node] = np.random.rand(30) * 36
            elif i == 4:
                data[node] = np.random.rand(30) * 33

        # Make a data frame
        df = pd.DataFrame(data)

        plt.clf()
        # style
        plt.style.use('seaborn-darkgrid')

        # create a color palette
        palette = plt.get_cmap('Set1')

        # multiple line plot
        num = 0
        for column in df.drop('x', axis=1):
            num += 1
            plt.plot(df['x'], df[column], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)

        # Add legend
        plt.legend(loc=2, ncol=2)

        # Add titles
        plt.title("Memory Usage({}~{})".format(date_list[-1], date_list[0]),
                  loc='left', fontsize=12, fontweight=0, color='green')
        plt.xlabel("Date")
        plt.ylabel("Memory Usage(%)")
        plt.axis([date_list[-1], date_list[0], 0, 100])
        plt.xticks(rotation=90)
        m_name = "{}{}{}.png".format(self.__save_dir, user_id, str(uuid1()))
        plt.savefig(m_name)

        return m_name

    def cpu_table(self, user_id, node_list):
        """
        CPU 사용량 테이블 생성
        :param user_id:
        :param node_list:
        :return:
        """
        date_list = list()
        for i in range(0, 30):
            d = datetime.now() - timedelta(days=i)
            date_list.append(d.strftime('%m/%d'))

        title_text = "CPU Usage({}~{})".format(date_list[-1], date_list[0])
        footer_text = "created {}".format(datetime.now().strftime('%Y.%m.%d %H:%M:%S'))
        fig_background_color = 'white'
        fig_border = 'white'
        data = list()

        data.append(node_list)

        data_tmp = list()

        for i, _ in enumerate(node_list):
            if i == 0:
                data_tmp.append(np.random.rand(30) * 10)
            elif i == 1:
                data_tmp.append(np.random.rand(30) * 12)
            elif i == 2:
                data_tmp.append(np.random.rand(30) * 14)
            elif i == 3:
                data_tmp.append(np.random.rand(30) * 16)
            elif i == 4:
                data_tmp.append(np.random.rand(30) * 13)

        data_arr = np.array(data_tmp)
        t_data_arr = data_arr.T

        for i, date in enumerate(date_list):
            tmp = list()
            tmp.append(date)
            sum_tmp = tmp + t_data_arr[i].tolist()
            print(sum_tmp)
            data.append(sum_tmp)

        plt.clf()
        column_headers = data.pop(0)
        row_headers = [x.pop(0) for x in data]
        cell_text = []
        for row in data:
            cell_text.append([f'{x:1.1f}' for x in row])
        rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
        ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
        my_dip = 96
        plt.figure(linewidth=2,
                   edgecolor=fig_border,
                   facecolor=fig_background_color,
                   tight_layout={'pad': 1},
                   figsize=(800/my_dip, 1300/my_dip)
                   )  # Add a table at the bottom of the axes
        the_table = plt.table(cellText=cell_text,
                              rowLabels=row_headers,
                              rowColours=rcolors,
                              rowLoc='right',
                              colColours=ccolors,
                              colLabels=column_headers,
                              loc='center')
        the_table.scale(1, 1.5)  # Hide axes
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)  # Hide axes border
        plt.box(on=None)  # Add title
        plt.suptitle(title_text)  # Add footer
        plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=6, weight='light')
        plt.draw()
        fig = plt.gcf()
        c_name = "{}{}{}.png".format(self.__save_dir, user_id, str(uuid1()))
        plt.savefig(c_name, edgecolor=fig.get_edgecolor(),
                    facecolor=fig.get_facecolor(), dpi=my_dip)
        return c_name

    def mem_table(self, user_id, node_list):
        """
        Memory 사용량 테이블 생성
        :param user_id:
        :param node_list:
        :return:
        """
        date_list = list()
        for i in range(0, 30):
            d = datetime.now() - timedelta(days=i)
            date_list.append(d.strftime('%m/%d'))

        title_text = "Memory Usage({}~{})".format(date_list[-1], date_list[0])
        footer_text = "created {}".format(datetime.now().strftime('%Y.%m.%d %H:%M:%S'))
        fig_background_color = 'white'
        fig_border = 'white'
        data = list()

        data.append(node_list)

        data_tmp = list()

        for i, _ in enumerate(node_list):
            if i == 0:
                data_tmp.append(np.random.rand(30) * 30)
            elif i == 1:
                data_tmp.append(np.random.rand(30) * 32)
            elif i == 2:
                data_tmp.append(np.random.rand(30) * 34)
            elif i == 3:
                data_tmp.append(np.random.rand(30) * 36)
            elif i == 4:
                data_tmp.append(np.random.rand(30) * 33)

        data_arr = np.array(data_tmp)
        t_data_arr = data_arr.T

        for i, date in enumerate(date_list):
            tmp = list()
            tmp.append(date)
            sum_tmp = tmp + t_data_arr[i].tolist()
            print(sum_tmp)
            data.append(sum_tmp)

        plt.clf()
        column_headers = data.pop(0)
        row_headers = [x.pop(0) for x in data]
        cell_text = []
        for row in data:
            cell_text.append([f'{x:1.1f}' for x in row])
        rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
        ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
        my_dip = 96
        plt.figure(linewidth=2,
                   edgecolor=fig_border,
                   facecolor=fig_background_color,
                   tight_layout={'pad': 1},
                   figsize=(800/my_dip, 1300/my_dip)
                   )  # Add a table at the bottom of the axes
        the_table = plt.table(cellText=cell_text,
                              rowLabels=row_headers,
                              rowColours=rcolors,
                              rowLoc='right',
                              colColours=ccolors,
                              colLabels=column_headers,
                              loc='center')
        the_table.scale(1, 1.5)  # Hide axes
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)  # Hide axes border
        plt.box(on=None)  # Add title
        plt.suptitle(title_text)  # Add footer
        plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=6, weight='light')
        plt.draw()
        fig = plt.gcf()
        m_name = "{}{}{}.png".format(self.__save_dir, user_id, str(uuid1()))
        plt.savefig(m_name, edgecolor=fig.get_edgecolor(),
                    facecolor=fig.get_facecolor(), dpi=my_dip)
        return m_name


if __name__ == "__main__":
    rg = SysReportGenerator()
    cu_img = rg.cpu_report('user1', ['n1', 'n2', 'n3'])
    ct_img = rg.cpu_table('user1', ['n1', 'n2', 'n3'])
    # print(file_name)
    # file_name = rg.mem_report('user1', ['n1', 'n2', 'n3'])
    # print(file_name)
