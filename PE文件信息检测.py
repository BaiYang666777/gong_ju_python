
import os
import hashlib
import pefile
import datetime
import sys


def gethash(file):
    m = hashlib.md5()
    s = hashlib.sha1()
    s256 = hashlib.sha256()
    with open(file,'rb') as f:
        for line in f:
            m.update(line)
            s.update(line)
            s256.update(line)
    md5code = m.hexdigest()
    sha1code = s.hexdigest()
    sha256code = s256.hexdigest()
    return (md5code,sha1code,sha256code)

def getPEinfo(myfile):
    pe = pefile.PE(myfile)
    warning = pe.get_warnings()
    mymd5code,mysha1code,mysha256code = gethash(myfile)
    print("查询文件: ",myfile)
    print('MD5: ',mymd5code)
    print('SHA-1:',mysha1code)
    print('SHA-256:',mysha256code)
    print('文件名字: ',os.path.basename(myfile))
    print('文件大小: ',os.path.getsize(myfile),'byte')
    print('可选映像头(Optional Header): ',hex(pe.OPTIONAL_HEADER.ImageBase))
    print('文件入口点(EntryPoint): ',pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    print("内存中的区块对其大小:"+hex(pe.OPTIONAL_HEADER.SectionAlignment))
    print("文件中的区块对其大小:"+hex(pe.OPTIONAL_HEADER.FileAlignment))
    print('编译时间: ',datetime.datetime.fromtimestamp(pe.FILE_HEADER.TimeDateStamp))
    print('子系统,入口函数(Subsystem): ',pefile.SUBSYSTEM_TYPE[pe.OPTIONAL_HEADER.Subsystem])
    print('DLL:',pe.FILE_HEADER.IMAGE_FILE_DLL)
    print('区段(Sections): ',pe.FILE_HEADER.NumberOfSections)
    print("导入DLL：")
    print("========================")
    for importdll in pe.DIRECTORY_ENTRY_IMPORT:
        print(importdll.dll.decode())
    print("========================")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python3 xxx.py xxx.exe")
        print("xxx.exe xxx.exe")
    else:
        try:
            getPEinfo(sys.argv[1]) 
        except FileNotFoundError:
            print("[-]找不到目标文件，存在空格需要双引号包裹")

