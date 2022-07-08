import pickle
import os
import os.path
import subprocess
import pexpect
import re
dict_data = {}


def clearBlankLine(src_file, dst_file):
    file1 = open(src_file, 'r', encoding='utf-8')
    file2 = open('new.conf', 'w', encoding='utf-8')

    try:
        for line in file1.readlines():
            if (line.startswith('#')):
                continue
            if(line.startswith('	')):
                continue
            if(line.startswith('    ')):
                continue
            if line == '\n':
                line = line.strip("\n")
            string = line
            file2.write(string.split('#')[0]+'\n')

    finally:
        file1.close()
        file2.close()

    file3 = open('new.conf', 'r', encoding='utf-8')
    file4 = open(dst_file, 'w', encoding='utf-8')

    try:
        for line in file3.readlines():
            if line == '\n':
                line = line.strip("\n")
            file4.write(line)
    finally:
        file3.close()
        file4.close()

    file5 = open(dst_file, 'r', encoding='utf-8')
    for line in file5.readlines():
        line = str(line).replace("\n", "")
        dict_data[line.split('=', 1)[0]] = line.split('=', 1)[1]
        ''' print(dict_data) '''

    file5.close()


# 从结果文件中读取吞吐量
def read_tpmC(file_path=None):
    if not os.path.exists(file_path):
        print("result file does not exitsts")
    res_file =  open(file_path,'r',encoding='utf8')
    num = 0
    for line in res_file.readlines():
        line = line.split()
        for i,item in enumerate(line):
            if item=='tpmTOTAL':
               num = line[i+2]
               break
    return num

def get_tmp_log(file_path):
    '''
    从文件中读取吞吐量
    :param file_path:
    :return:
    '''


if __name__ == "__main__":
    # 生成配置文件
    # clearBlankLine('props.opengauss.1000w','new1.conf')

    # 完成配置文件生效
    subprocess.run(["docker","restart","opengauss3"])

    log_file = "log_run.txt"
    # 运行测试，日志结果写入另一个文件
    subprocess.run(["./runDatabaseDestroy.sh", "props.opengauss.1000w"])
    subprocess.run(["./runDatabaseBuild.sh" ,"props.opengauss.1000w"])
    subprocess.run(args=["./runBenchmark.sh","props.opengauss.1000w"],
                   stdout=open(log_file,'w',encoding='utf8'), text=True)

    print('test completed, start extracting')
    pat_tmpc = re.compile(r'Measured tpmC (NewOrders) = \d+\.\d+')
    pat_tmpc_num = re.compile(r"\d+\.\d+")
    print('reg compile completed')

    with open(log_file,'r',encoding='utf8') as f:
        lines = f.readlines()
        # print(lines)
        for line in lines:
            print(line)
            if line == '\n':
                continue
            result = pat_tmpc.findall(line)
            if result == []:
                continue
            print(result)
            # tmpc = pat_tmpc_num.findall(result[0])[0]
            tmpc = pat_tmpc_num.search(r"\d+\.\d+", result[0])
            print(tmpc)


    # with open('dict_data.pickle', 'wb') as f:
    #     pickle.dump(dict_data, f, pickle.HIGHEST_PROTOCOL)
    # with open('dict_data.pickle', 'rb') as f:
    #     data = pickle.load(f)


