====
설치
====

이것은 Python을 기반으로 구현되었습니다. 3. 파이썬을 설치하기 전에, 파이썬 라이브러리를
추가로 설치해야합니다. 설치 지침은 각 플랫폼마다 약간 씩 다릅니다.

-----
리눅스
-----


Python3과 PyQt5가 필요합니다. 두 가지 모두 설치되어있을 가능성이 있습니다. 배포본이
Debian / Ubuntu를 기반으로하는 경우 다음 명령을 실행하면 필요한 모든 라이브러리가 설치됩니다.

::

    $ sudo apt-get install python3-all python3-pyqt5 python3-pyqt5.qsci
      python3-pyqt5.qtsvg python3-pyqt5.qtwebkit python3-pip
        
로컬 설치 만 수행하려는 경우 명령은 다음과 같습니다

::

    $ pip3 install pytunol --user

(모든 사용자에 대해 설치하려면 --user 옵션을 무시하십시오.이 경우 *sudo* 와 같은 명령을
실행해야합니다.). 설치가 끝나면 다음을 실행하여 PyKor 버전을 업데이트 할 수 있습니다

::
    $ pip3 install pytunol -U --user

설치 스크립트는 실행 파일을 ``~/.local/bin.`` 폴더와 ``/bin/``폴더 (있는 경우)에
저장합니다.

-------
Windows
-------

수행 할...
