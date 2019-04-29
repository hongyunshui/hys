# hys

# oracle linux 6.5 安装oracle 11g R2 rac集群
  实验环境 <br>
  虚拟化软件virtualBox <br>
虚拟机操作系统oracle linux 6.5 <br>
虚拟机双网口 <br>
一个public network <br>
一个prviate network/jlib <br>
磁盘30G，分配的时候，6G留给交换分区，其他全部划分到根目录下 <br>

# 1.操作系统以及依赖安装
安装操作系统时需勾选的选项
    Base System > Base
    Base System > Compatibility libraries
    Base System > Hardware monitoring utilities
Base System > Large Systems Performance
Base System > Network file system client
Base System > Performance Tools
Base System > Perl Support
Servers > Server Platform
Servers > System administration tools
Desktops > Desktop
Desktops > Desktop Platform
Desktops > Fonts
Desktops > General Purpose Desktop
Desktops > Graphical Administration Tools
Desktops > Input Methods
Desktops > X Window System
Applications > Internet Browser
Development > Additional Development
Development > Development Tools

# 2.挂载镜像
    mkdir /media/cdrom
    mount /dev/cdrom/ /media/cdrom

# 3.安装所需的包
cd /mdeia/cdrom
cd /media/OL6.5\ x86_64\ Disc\ 1\ 20131125/Packages/
rpm -Uvh binutils-2.*
rpm -Uvh compat-libstdc++-33-3.2.3-69.el6.i686.rpm 
rpm -Uvh compat-libstdc++-33-3.2.3-69.el6.x86_64.rpm 
rpm -Uvh elfutils-libelf-0.152-1.el6.i686.rpm 
rpm -Uvh elfutils-libelf-0.152-1.el6.x86_64.rpm 
rpm -Uvh libaio-0.3.107-10.el6.i686.rpm 
rpm -Uvh libaio-0.3.107-10.el6.x86_64.rpm 
rpm -Uvh libaio-devel-0.3.107-10.el6.i686.rpm 
rpm -Uvh libaio-devel-0.3.107-10.el6.x86_64.rpm 
rpm -Uvh sysstat-9.0.4-22.el6.x86_64.rpm 
rpm -Uvh glibc-2.12-1.132.el6.i686.rpm 
rpm -Uvh glibc-2.12-1.132.el6.x86_64.rpm 
rpm -Uvh glibc-common-2.12-1.132.el6.x86_64.rpm 
rpm -Uvh glibc-devel-2.12-1.132.el6.x86_64.rpm
rpm -Uvh glibc-devel-2.12-1.132.el6.i686.rpm 
 rpm -Uvh glibc-headers-2.12-1.132.el6.x86_64.rpm 
rpm -Uvh ksh-20120801-10.el6.x86_64.rpm 
rpm -Uvh make-3.81-20.el6.x86_64.rpm 
rpm -Uvh libgcc-4.4.7-4.el6.i686.rpm 
rpm -Uvh libgcc-4.4.7-4.el6.x86_64.rpm 
rpm -Uvh libstdc++-4.4.7-4.el6.i686.rpm 
rpm -Uvh libstdc++-4.4.7-4.el6.x86_64.rpm 
rpm -Uvh gcc-4.4.7-4.el6.x86_64.rpm 
rpm -Uvh gcc-c++-4.4.7-4.el6.x86_64.rpm 
rpm -Uvh elfutils-libelf-0.152-1.el6.i686.rpm 
rpm -Uvh elfutils-libelf-0.152-1.el6.x86_64.rpm 
rpm -Uvh elfutils-libelf-devel-0.152-1.el6.i686.rpm 
rpm -Uvh elfutils-libelf-devel-0.152-1.el6.x86_64.rpm 
rpm -Uvh libtool-ltdl-2.2.6-15.5.el6.i686.rpm 
rpm -Uvh ncurses*i686*
rpm -Uvh readline*i686*
rpm -Uvh unixODBC*
可写成脚本在Package目录下执行

# 4.修改内核参数
vi /etc/sysctl.conf
fs.aio-max-nr = 1048576
fs.file-max = 6815744
kernel.shmmni = 4096
kernel.sem = 250 32000 100 128
net.ipv4.ip_local_port_range = 9000 65500
net.core.rmem_default=262144
net.core.rmem_max=4194304
net.core.wmem_default=262144
net.core.wmem_max=1048586
执行生效
sysctl -p
有报错
error: "net.bridge.bridge-nf-call-ip6tables" is an unknown key
error: "net.bridge.bridge-nf-call-iptables" is an unknown key
error: "net.bridge.bridge-nf-call-arptables" is an unknown key
加载内核模块
modprobe bridge
sysctl -p

# 5.修改用户限制
vi /etc/security/limits.conf
//
oracle              soft    nproc   2047
oracle              hard    nproc   16384
oracle              soft    nofile  4096
oracle              hard    nofile  65536
oracle              soft    stack   10240
oracle              soft    memlock 10485760
orcale              hard    memlock 10485760

grid              soft    nproc   2047
grid              hard    nproc   16384
grid              soft    nofile  4096
grid              hard    nofile  65536
grid              soft    stack   10240
//

# 6.修改文件
vi /etc/pam.d/login 
//
session    required     pam_limits.so
//

# 7.关闭防火墙及SElinux
sed -i 's/enforcing/disabled/g' /etc/selinux/config 
setenforce 0
chkconfig iptables off
service iptables stop

# 8.创建oracle所需用户和用户组
/usr/sbin/groupadd -g 1000 oinstall 
/usr/sbin/groupadd -g 1020 asmadmin 
/usr/sbin/groupadd -g 1021 asmdba 
/usr/sbin/groupadd -g 1022 asmoper 
/usr/sbin/groupadd -g 1031 dba 
/usr/sbin/groupadd -g 1032 oper
/usr/sbin/useradd -g oinstall -G asmadmin,asmdba,asmoper,oper,dba -u 1100 grid 
/usr/sbin/useradd -g oinstall -G dba,asmdba,oper -u 1101 oracle
然后修改oracle和grid密码

# 9.在grid和oracle用户下配置互信
test01节点
ssh-keygen -t dsa
ssh-copy-id -i .ssh/id_dsa.pub test01
ssh-copy-id -i .ssh/id_dsa.pub test02
test02节点
ssh-keygen -t dsa
ssh-copy-id -i .ssh/id_dsa.pub test01
ssh-copy-id -i .ssh/id_dsa.pub test02

# 10.修改oracle和grid环境变量
oracle环境变量
节点1
ORACLE_SID=orcl1; export ORACLE_SID
ORACLE_BASE=/u01/app/oracle; export ORACLE_BASE
ORACLE_HOME=$ORACLE_BASE/product/11.2.0/db_1; export ORACLE_HOME
PATH=${PATH}:/usr/bin:/bin:/sbin:/usr/bin/X11:/usr/local/bin:$ORACLE_HOME/bin
PATH=${PATH}:/oracle/product/common/oracle/bin
export PATH

LD_LIBRARY_PATH=$ORACLE_HOME/lib
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$ORACLE_HOME/oracm/lib
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/lib:/usr/lib:/usr/local/lib
export LD_LIBRARY_PATH

CLASSPATH=$ORACLE_HOME/JRE
CLASSPATH=${CLASSPATH}:$ORACLE_HOME/jlib
CLASSPATH=${CLASSPATH}:$ORACLE_HOME/rdbms/jlib
CLASSPATH=${CLASSPATH}:$ORACLE_HOME/network/jlib
export CLASSPATH

export TEMP=/tmp
export TMPDIR=/tmp
umask 022
节点2
ORACLE_SID=orcl2; export ORACLE_SID
ORACLE_BASE=/u01/app/oracle; export ORACLE_BASE
ORACLE_HOME=$ORACLE_BASE/product/11.2.0/db_1; export ORACLE_HOME
PATH=${PATH}:/usr/bin:/bin:/sbin:/usr/bin/X11:/usr/local/bin:$ORACLE_HOME/bin
PATH=${PATH}:/oracle/product/common/oracle/bin
export PATH

LD_LIBRARY_PATH=$ORACLE_HOME/lib
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$ORACLE_HOME/oracm/lib
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/lib:/usr/lib:/usr/local/lib
export LD_LIBRARY_PATH

CLASSPATH=$ORACLE_HOME/JRE
CLASSPATH=${CLASSPATH}:$ORACLE_HOME/jlib
CLASSPATH=${CLASSPATH}:$ORACLE_HOME/rdbms/jlib
CLASSPATH=${CLASSPATH}:$ORACLE_HOME/network/jlib
export CLASSPATH

export TEMP=/tmp
export TMPDIR=/tmp
umask 022
grid环境变量
export ORACLE_HOME=/u01/app/11.2.0/grid
export PATH=$ORACLE_HOME/bin:$ORACLE_HOME/OPatch:/sbin:/bin:/usr/sbin:/usr/bin

export ORACLE_SID=+ASM2
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$ORACLE_HOME/lib32

export ORACLE_BASE=/u01/app/grid
export ORA_NLS10=$ORACLE_HOME/nls/data
export NLS_LANG=american_america.AL32UTF8 

CLASSPATH=$ORACLE_HOME/JRE
CLASSPATH=${CLASSPATH}:$ORACLE_HOME/jlib
CLASSPATH=${CLASSPATH}:$ORACLE_HOME/rdbms/jlib
CLASSPATH=${CLASSPATH}:$ORACLE_HOME/network/jlib
export CLASSPATH


SID根据实际情况选择

# 11.时钟同步配置
vi /etc/sysconfig/ntpd
OPTIONS="-x -u ntp:ntp -p /var/run/ntpd.pid -g"
其中一个节点和外部时钟服务器同步，另一个同步到这个节点
本例中test01和外部同步，test02和test01同步
//

# 12.共享存储创建
创建完成后分区

    /sbin/scsi_id -g -u -d /dev/sdb1
  /sbin/scsi_id -g -u -d /dev/sdc1
   /sbin/scsi_id -g -u -d /dev/sdd1
  /sbin/scsi_id -g -u -d /dev/sde1
  /sbin/scsi_id -g -u -d /dev/sdf1
udev绑定磁盘路径和权限

 vi /etc/udev/rules.d/99-oracle-asmdevices.rules
KERNEL=="sd*", BUS=="scsi", PROGRAM=="/sbin/scsi_id -g -u -d /dev/$parent", RESULT=="1ATA_VBOX_HARDDISK_VB67713a3b-d1
448e77",NAME="asm-disk1", OWNER="grid", GROUP="asmadmin", MODE="0660"
KERNEL=="sd*", BUS=="scsi", PROGRAM=="/sbin/scsi_id -g -u -d /dev/$parent", RESULT=="1ATA_VBOX_HARDDISK_VB6b88618f-dc
ac53c7",NAME="asm-disk2", OWNER="grid", GROUP="asmadmin", MODE="0660"
KERNEL=="sd*", BUS=="scsi", PROGRAM=="/sbin/scsi_id -g -u -d /dev/$parent", RESULT=="1ATA_VBOX_HARDDISK_VB8e0e340e-bc
75d7d4",NAME="asm-disk3", OWNER="grid", GROUP="asmadmin", MODE="0660"
KERNEL=="sd*", BUS=="scsi", PROGRAM=="/sbin/scsi_id -g -u -d /dev/$parent", RESULT=="1ATA_VBOX_HARDDISK_VBb7a7ff67-64
0abe54",NAME="asm-disk4", OWNER="grid", GROUP="asmadmin", MODE="0660"
KERNEL=="sd*", BUS=="scsi", PROGRAM=="/sbin/scsi_id -g -u -d /dev/$parent", RESULT=="1ATA_VBOX_HARDDISK_VB2bd1aa20-86
735a83",NAME="asm-disk5", OWNER="grid", GROUP="asmadmin", MODE="0660"

# 13.创建相关目录

mkdir -p /u01/app/11.2.0/grid
 mkdir -p /u01/app/oracle/product/11.2.0/db_1
chown -R oracle:oinstall /u01/
chmod -R 775 /u01/




