#!/usr/bin/env bash

###########################
# user-defined commands
###########################

# softwares
alias topcat="java -jar $HOME/mysoftware/topcat-full.jar &"
alias pycharm="bash $HOME/mysoftware/pycharm/pycharm-community-2017.2/bin/pycharm.sh &"
alias jupyter-font="jupyter-qtconsole --ConsoleWidget.font_size=13 &"

# python profile
alias kernprof="$HOME/.local/lib/python2.7/site-packages/kernprof.py"

# apt-get-fix
alias apt-fix="sudo rm -rf /var/lib/dpkg/info.bak; sudo mv /var/lib/dpkg/info /var/lib/dpkg/info.bak; sudo mkdir /var/lib/dpkg/info; sudo apt-get update"
alias conda2="source $HOME/anaconda2/bin/activate"
alias conda2close="source $HOME/anaconda2/bin/deactivate"
alias jenkins="java -jar $HOME/mysoftware/jenkins/jenkins.war"
alias juliapro="$HOME/juliapro/JuliaPro-0.5.1.1/julia"
alias juno="$HOME/juliapro/JuliaPro-0.5.1.1/Juno"
alias matlab2016post="sudo mv /usr/lib/nvidia-361/libGLX_nvidia.so.0.old /usr/lib/nvidia-361/libGLX_nvidia.so.0"
alias matlab2016pre="sudo mv /usr/lib/nvidia-361/libGLX_nvidia.so.0 /usr/lib/nvidia-361/libGLX_nvidia.so.0.old "
alias matlab_2014a="/share/apps/matlab2014a/bin/matlab &"
alias __xgterm="xgterm -sl 20000 -fg green -bg black -cr red -fn 9*15 &"
alias vncserver1="vncserver -geometry 1920x1010 :1"
alias vncserver2="vncserver -geometry 1920x1010 :2"
alias vncserver7="vncserver -geometry 1920x1010 :7"
alias vncserver77="vncserver -geometry 1920x1010 :77"
alias vncserver99="vncserver -geometry 1920x1010 :99"
alias vncconfig_blacklist1="vncconfig -display :1 -set BlackListTimeout=0 -set BlackListThreshold=9999999999"
alias vncconfig_blacklist2="vncconfig -display :2 -set BlackListTimeout=0 -set BlackListThreshold=9999999999"


###########################
# ssh #
###########################
# T7610
alias ssh-t7610="ssh -X cham@10.25.1.131"
# chenxy
alias ssh-chenxy="ssh -X chenxy@10.25.1.43"
alias ssh-chenxy-cham="ssh -X cham@10.25.1.43"
# lcq
alias ssh-lcq="ssh -X lcq@10.25.1.30"
# ali ECS VM
alias ssh-ali-root="ssh -X -Y root@101.201.56.181 -p 9990"
alias ssh-ali="ssh -X -Y cham@101.201.56.181 -p 9990"
# zen
alias ssh-zen="ssh -X zb@10.0.10.94"
alias ssh-zen-ex="ssh -X zb@zen.bao.ac.cn"
alias ssh-zen-chenxy="ssh -X xychen@10.0.10.94"
# zen nodes
alias ssh1="ssh -X -Y zen-0-1"
alias ssh2="ssh -X -Y zen-0-2"
alias ssh3="ssh -X -Y zen-0-3"
alias ssh4="ssh -X -Y zen-0-4"
alias ssh5="ssh -X -Y zen-0-5"
alias ssh6="ssh -X -Y zen-0-6"
alias ssh7="ssh -X -Y zen-0-7"
alias ssh8="ssh -X -Y zen-0-8"
alias ssh9="ssh -X -Y zen-0-9"
alias ssh10="ssh -X -Y zen-0-10"
alias ssh11="ssh -X -Y zen-0-11"
alias ssh12="ssh -X -Y zen-0-12"
alias ssh13="ssh -X -Y zen-0-13"
alias ssh14="ssh -X -Y zen-0-14"
alias ssh15="ssh -X -Y zen-0-15"
alias ssh16="ssh -X -Y zen-0-16"


###########################
# UREKA
###########################
ur_setup() {
    eval `$HOME/.ureka/ur_setup -sh $*`
}
ur_forget() {
    eval `$HOME/.ureka/ur_forget -sh $*`
}
#ur_setup


###########################
# user-defined paths
###########################

# mycommand --> deprecated
# export PATH="$HOME/mycommand:$PATH"

# Anaconda2
# export PATH="$HOME/anaconda2/bin:$PATH"

# added by Anaconda3 4.2.0 installer
export PATH="$HOME/anaconda3/bin:$PATH"
export PYTHONPATH="$HOME/anaconda3/lib/python3.6/site-packages"

# added by PyCharm
export PATH="$HOME/mysoftware/pycharm/pycharm-community-2017.2/bin/:$PATH"

# STELLA
export PATH="$HOME/bin:$PATH"

# ################
# T7610
####################

# Montage
export PATH="$PATH:$HOME/mysoftware/montage/Montage/bin"

# open MPI
export LD_LIBRARY_PATH="/usr/lib/openmpi/lib/"
export PATH="$PATH:$HOME/.openmpi/bin"

# LIBSVM
export PATH="$HOME/mysoftware/svm/libsvm:$PATH"
export PYTHONPATH="$HOME/mysoftware/svm/libsvm/python:$PYTHONPATH"

# Julia
export JULIA_HOME="$HOME/juliapro/JuliaPro-0.5.1.1/Julia/bin"

# github oauth
export GITHUB_CLIENT_ID=c8c94e4c16c8a2afddc2
export GITHUB_CLIENT_SECRET=3d5bf163bb3a35567edab29c2a3cd8de2d105cfc
export OAUTH_CALLBACK_URL=https://hypergravity.jupyter.org/hub/oauth_callback
