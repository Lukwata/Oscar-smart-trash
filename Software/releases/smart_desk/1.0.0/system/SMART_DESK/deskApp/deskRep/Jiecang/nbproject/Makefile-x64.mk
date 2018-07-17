#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Environment
MKDIR=mkdir
CP=cp
GREP=grep
NM=nm
CCADMIN=CCadmin
RANLIB=ranlib
CC=gcc
CCC=g++
CXX=g++
FC=gfortran
AS=as

# Macros
CND_PLATFORM=GNU-Linux
CND_DLIB_EXT=so
CND_CONF=x64
CND_DISTDIR=dist
CND_BUILDDIR=build

# Include project Makefile
include Makefile

# Object Directory
OBJECTDIR=${CND_BUILDDIR}/${CND_CONF}/${CND_PLATFORM}

# Object Files
OBJECTFILES= \
	${OBJECTDIR}/user/main.o \
	${OBJECTDIR}/user/src/DeskComm.o \
	${OBJECTDIR}/user/src/DeskManager.o \
	${OBJECTDIR}/user/src/MySerial.o \
	${OBJECTDIR}/user/src/MyZMQ.o \
	${OBJECTDIR}/user/src/Thread.o

# Test Directory
TESTDIR=${CND_BUILDDIR}/${CND_CONF}/${CND_PLATFORM}/tests

# Test Files
TESTFILES= \
	user/x64/deskrep_test

# Test Object Files
TESTOBJECTFILES= \
	${TESTDIR}/tests/MySerialrunner.o \
	${TESTDIR}/tests/testMyserialclass.o

# C Compiler Flags
CFLAGS=

# CC Compiler Flags
CCFLAGS=
CXXFLAGS=

# Fortran Compiler Flags
FFLAGS=

# Assembler Flags
ASFLAGS=

# Link Libraries and Options
LDLIBSOPTIONS=-lpthread `pkg-config --libs libzmq`  

# Build Targets
.build-conf: ${BUILD_SUBPROJECTS}
	"${MAKE}"  -f nbproject/Makefile-${CND_CONF}.mk user/x64/deskrep

user/x64/deskrep: ${OBJECTFILES}
	${MKDIR} -p user/x64
	${LINK.cc} -o user/x64/deskrep ${OBJECTFILES} ${LDLIBSOPTIONS}

${OBJECTDIR}/user/main.o: user/main.cpp
	${MKDIR} -p ${OBJECTDIR}/user
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc `pkg-config --cflags libzmq` -std=c++11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/main.o user/main.cpp

${OBJECTDIR}/user/src/DeskComm.o: user/src/DeskComm.cpp
	${MKDIR} -p ${OBJECTDIR}/user/src
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc `pkg-config --cflags libzmq` -std=c++11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/DeskComm.o user/src/DeskComm.cpp

${OBJECTDIR}/user/src/DeskManager.o: user/src/DeskManager.cpp
	${MKDIR} -p ${OBJECTDIR}/user/src
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc `pkg-config --cflags libzmq` -std=c++11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/DeskManager.o user/src/DeskManager.cpp

${OBJECTDIR}/user/src/MySerial.o: user/src/MySerial.cpp
	${MKDIR} -p ${OBJECTDIR}/user/src
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc `pkg-config --cflags libzmq` -std=c++11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/MySerial.o user/src/MySerial.cpp

${OBJECTDIR}/user/src/MyZMQ.o: user/src/MyZMQ.cpp
	${MKDIR} -p ${OBJECTDIR}/user/src
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc `pkg-config --cflags libzmq` -std=c++11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/MyZMQ.o user/src/MyZMQ.cpp

${OBJECTDIR}/user/src/Thread.o: user/src/Thread.cpp
	${MKDIR} -p ${OBJECTDIR}/user/src
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc `pkg-config --cflags libzmq` -std=c++11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/Thread.o user/src/Thread.cpp

# Subprojects
.build-subprojects:

# Build Test Targets
.build-tests-conf: .build-tests-subprojects .build-conf ${TESTFILES}
.build-tests-subprojects:

user/x64/deskrep_test: ${TESTDIR}/tests/MySerialrunner.o ${TESTDIR}/tests/testMyserialclass.o ${OBJECTFILES:%.o=%_nomain.o}
	${MKDIR} -p user/x64
	${LINK.cc} -o user/x64/deskrep_test $^ ${LDLIBSOPTIONS}   -lpthread `pkg-config --libs libzmq`   `cppunit-config --libs` -ldl  -lpthread  `pkg-config --libs libzmq`   


${TESTDIR}/tests/MySerialrunner.o: tests/MySerialrunner.cpp 
	${MKDIR} -p ${TESTDIR}/tests
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc -Iuser/inc -Iuser/inc `pkg-config --cflags libzmq` -std=c++11 `cppunit-config --cflags` -MMD -MP -MF "$@.d" -o ${TESTDIR}/tests/MySerialrunner.o tests/MySerialrunner.cpp


${TESTDIR}/tests/testMyserialclass.o: tests/testMyserialclass.cpp 
	${MKDIR} -p ${TESTDIR}/tests
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc -Iuser/inc -Iuser/inc `pkg-config --cflags libzmq` -std=c++11 `cppunit-config --cflags` -MMD -MP -MF "$@.d" -o ${TESTDIR}/tests/testMyserialclass.o tests/testMyserialclass.cpp


${OBJECTDIR}/user/main_nomain.o: ${OBJECTDIR}/user/main.o user/main.cpp 
	${MKDIR} -p ${OBJECTDIR}/user
	@NMOUTPUT=`${NM} ${OBJECTDIR}/user/main.o`; \
	if (echo "$$NMOUTPUT" | ${GREP} '|main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T _main$$'); \
	then  \
	    ${RM} "$@.d";\
	    $(COMPILE.cc) -g -Iuser/inc `pkg-config --cflags libzmq` -std=c++11  -Dmain=__nomain -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/main_nomain.o user/main.cpp;\
	else  \
	    ${CP} ${OBJECTDIR}/user/main.o ${OBJECTDIR}/user/main_nomain.o;\
	fi

${OBJECTDIR}/user/src/DeskComm_nomain.o: ${OBJECTDIR}/user/src/DeskComm.o user/src/DeskComm.cpp 
	${MKDIR} -p ${OBJECTDIR}/user/src
	@NMOUTPUT=`${NM} ${OBJECTDIR}/user/src/DeskComm.o`; \
	if (echo "$$NMOUTPUT" | ${GREP} '|main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T _main$$'); \
	then  \
	    ${RM} "$@.d";\
	    $(COMPILE.cc) -g -Iuser/inc `pkg-config --cflags libzmq` -std=c++11  -Dmain=__nomain -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/DeskComm_nomain.o user/src/DeskComm.cpp;\
	else  \
	    ${CP} ${OBJECTDIR}/user/src/DeskComm.o ${OBJECTDIR}/user/src/DeskComm_nomain.o;\
	fi

${OBJECTDIR}/user/src/DeskManager_nomain.o: ${OBJECTDIR}/user/src/DeskManager.o user/src/DeskManager.cpp 
	${MKDIR} -p ${OBJECTDIR}/user/src
	@NMOUTPUT=`${NM} ${OBJECTDIR}/user/src/DeskManager.o`; \
	if (echo "$$NMOUTPUT" | ${GREP} '|main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T _main$$'); \
	then  \
	    ${RM} "$@.d";\
	    $(COMPILE.cc) -g -Iuser/inc `pkg-config --cflags libzmq` -std=c++11  -Dmain=__nomain -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/DeskManager_nomain.o user/src/DeskManager.cpp;\
	else  \
	    ${CP} ${OBJECTDIR}/user/src/DeskManager.o ${OBJECTDIR}/user/src/DeskManager_nomain.o;\
	fi

${OBJECTDIR}/user/src/MySerial_nomain.o: ${OBJECTDIR}/user/src/MySerial.o user/src/MySerial.cpp 
	${MKDIR} -p ${OBJECTDIR}/user/src
	@NMOUTPUT=`${NM} ${OBJECTDIR}/user/src/MySerial.o`; \
	if (echo "$$NMOUTPUT" | ${GREP} '|main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T _main$$'); \
	then  \
	    ${RM} "$@.d";\
	    $(COMPILE.cc) -g -Iuser/inc `pkg-config --cflags libzmq` -std=c++11  -Dmain=__nomain -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/MySerial_nomain.o user/src/MySerial.cpp;\
	else  \
	    ${CP} ${OBJECTDIR}/user/src/MySerial.o ${OBJECTDIR}/user/src/MySerial_nomain.o;\
	fi

${OBJECTDIR}/user/src/MyZMQ_nomain.o: ${OBJECTDIR}/user/src/MyZMQ.o user/src/MyZMQ.cpp 
	${MKDIR} -p ${OBJECTDIR}/user/src
	@NMOUTPUT=`${NM} ${OBJECTDIR}/user/src/MyZMQ.o`; \
	if (echo "$$NMOUTPUT" | ${GREP} '|main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T _main$$'); \
	then  \
	    ${RM} "$@.d";\
	    $(COMPILE.cc) -g -Iuser/inc `pkg-config --cflags libzmq` -std=c++11  -Dmain=__nomain -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/MyZMQ_nomain.o user/src/MyZMQ.cpp;\
	else  \
	    ${CP} ${OBJECTDIR}/user/src/MyZMQ.o ${OBJECTDIR}/user/src/MyZMQ_nomain.o;\
	fi

${OBJECTDIR}/user/src/Thread_nomain.o: ${OBJECTDIR}/user/src/Thread.o user/src/Thread.cpp 
	${MKDIR} -p ${OBJECTDIR}/user/src
	@NMOUTPUT=`${NM} ${OBJECTDIR}/user/src/Thread.o`; \
	if (echo "$$NMOUTPUT" | ${GREP} '|main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T _main$$'); \
	then  \
	    ${RM} "$@.d";\
	    $(COMPILE.cc) -g -Iuser/inc `pkg-config --cflags libzmq` -std=c++11  -Dmain=__nomain -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/Thread_nomain.o user/src/Thread.cpp;\
	else  \
	    ${CP} ${OBJECTDIR}/user/src/Thread.o ${OBJECTDIR}/user/src/Thread_nomain.o;\
	fi

# Run Test Targets
.test-conf:
	@if [ "${TEST}" = "" ]; \
	then  \
	    user/x64/deskrep_test || true; \
	else  \
	    ./${TEST} || true; \
	fi

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r ${CND_BUILDDIR}/${CND_CONF}

# Subprojects
.clean-subprojects:

# Enable dependency checking
.dep.inc: .depcheck-impl

include .dep.inc
