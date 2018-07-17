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
	${OBJECTDIR}/_ext/aff35550/AutonomousCommFrame.o \
	${OBJECTDIR}/user/src/DeskCmd.o \
	${OBJECTDIR}/user/src/MyZMQ.o \
	${OBJECTDIR}/user/src/main.o

# Test Directory
TESTDIR=${CND_BUILDDIR}/${CND_CONF}/${CND_PLATFORM}/tests

# Test Files
TESTFILES= \
	${TESTDIR}/TestFiles/f1

# Test Object Files
TESTOBJECTFILES= \
	${TESTDIR}/tests/newtestclass.o \
	${TESTDIR}/tests/newtestrunner.o

# C Compiler Flags
CFLAGS=-m64

# CC Compiler Flags
CCFLAGS=-m64
CXXFLAGS=-m64

# Fortran Compiler Flags
FFLAGS=

# Assembler Flags
ASFLAGS=

# Link Libraries and Options
LDLIBSOPTIONS=`pkg-config --libs libzmq` -ldl  -lpthread   

# Build Targets
.build-conf: ${BUILD_SUBPROJECTS}
	"${MAKE}"  -f nbproject/Makefile-${CND_CONF}.mk user/x64/agingtest

user/x64/agingtest: ${OBJECTFILES}
	${MKDIR} -p user/x64
	g++ -o user/x64/agingtest ${OBJECTFILES} ${LDLIBSOPTIONS}

${OBJECTDIR}/_ext/aff35550/AutonomousCommFrame.o: /home/thanh/ws/Linux/myLib/Library/src/Device/AutonomousCommFrame.c
	${MKDIR} -p ${OBJECTDIR}/_ext/aff35550
	${RM} "$@.d"
	$(COMPILE.c) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/aff35550/AutonomousCommFrame.o /home/thanh/ws/Linux/myLib/Library/src/Device/AutonomousCommFrame.c

${OBJECTDIR}/user/src/DeskCmd.o: user/src/DeskCmd.cpp
	${MKDIR} -p ${OBJECTDIR}/user/src
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c++11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/DeskCmd.o user/src/DeskCmd.cpp

${OBJECTDIR}/user/src/MyZMQ.o: user/src/MyZMQ.cpp
	${MKDIR} -p ${OBJECTDIR}/user/src
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c++11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/MyZMQ.o user/src/MyZMQ.cpp

${OBJECTDIR}/user/src/main.o: user/src/main.cpp
	${MKDIR} -p ${OBJECTDIR}/user/src
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c++11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/main.o user/src/main.cpp

# Subprojects
.build-subprojects:

# Build Test Targets
.build-tests-conf: .build-tests-subprojects .build-conf ${TESTFILES}
.build-tests-subprojects:

${TESTDIR}/TestFiles/f1: ${TESTDIR}/tests/newtestclass.o ${TESTDIR}/tests/newtestrunner.o ${OBJECTFILES:%.o=%_nomain.o}
	${MKDIR} -p ${TESTDIR}/TestFiles
	${LINK.cc} -o ${TESTDIR}/TestFiles/f1 $^ ${LDLIBSOPTIONS}   `cppunit-config --libs`   


${TESTDIR}/tests/newtestclass.o: tests/newtestclass.cpp 
	${MKDIR} -p ${TESTDIR}/tests
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c++11 `cppunit-config --cflags` -MMD -MP -MF "$@.d" -o ${TESTDIR}/tests/newtestclass.o tests/newtestclass.cpp


${TESTDIR}/tests/newtestrunner.o: tests/newtestrunner.cpp 
	${MKDIR} -p ${TESTDIR}/tests
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c++11 `cppunit-config --cflags` -MMD -MP -MF "$@.d" -o ${TESTDIR}/tests/newtestrunner.o tests/newtestrunner.cpp


${OBJECTDIR}/_ext/aff35550/AutonomousCommFrame_nomain.o: ${OBJECTDIR}/_ext/aff35550/AutonomousCommFrame.o /home/thanh/ws/Linux/myLib/Library/src/Device/AutonomousCommFrame.c 
	${MKDIR} -p ${OBJECTDIR}/_ext/aff35550
	@NMOUTPUT=`${NM} ${OBJECTDIR}/_ext/aff35550/AutonomousCommFrame.o`; \
	if (echo "$$NMOUTPUT" | ${GREP} '|main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T _main$$'); \
	then  \
	    ${RM} "$@.d";\
	    $(COMPILE.c) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c11  -Dmain=__nomain -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/aff35550/AutonomousCommFrame_nomain.o /home/thanh/ws/Linux/myLib/Library/src/Device/AutonomousCommFrame.c;\
	else  \
	    ${CP} ${OBJECTDIR}/_ext/aff35550/AutonomousCommFrame.o ${OBJECTDIR}/_ext/aff35550/AutonomousCommFrame_nomain.o;\
	fi

${OBJECTDIR}/user/src/DeskCmd_nomain.o: ${OBJECTDIR}/user/src/DeskCmd.o user/src/DeskCmd.cpp 
	${MKDIR} -p ${OBJECTDIR}/user/src
	@NMOUTPUT=`${NM} ${OBJECTDIR}/user/src/DeskCmd.o`; \
	if (echo "$$NMOUTPUT" | ${GREP} '|main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T _main$$'); \
	then  \
	    ${RM} "$@.d";\
	    $(COMPILE.cc) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c++11  -Dmain=__nomain -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/DeskCmd_nomain.o user/src/DeskCmd.cpp;\
	else  \
	    ${CP} ${OBJECTDIR}/user/src/DeskCmd.o ${OBJECTDIR}/user/src/DeskCmd_nomain.o;\
	fi

${OBJECTDIR}/user/src/MyZMQ_nomain.o: ${OBJECTDIR}/user/src/MyZMQ.o user/src/MyZMQ.cpp 
	${MKDIR} -p ${OBJECTDIR}/user/src
	@NMOUTPUT=`${NM} ${OBJECTDIR}/user/src/MyZMQ.o`; \
	if (echo "$$NMOUTPUT" | ${GREP} '|main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T _main$$'); \
	then  \
	    ${RM} "$@.d";\
	    $(COMPILE.cc) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c++11  -Dmain=__nomain -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/MyZMQ_nomain.o user/src/MyZMQ.cpp;\
	else  \
	    ${CP} ${OBJECTDIR}/user/src/MyZMQ.o ${OBJECTDIR}/user/src/MyZMQ_nomain.o;\
	fi

${OBJECTDIR}/user/src/main_nomain.o: ${OBJECTDIR}/user/src/main.o user/src/main.cpp 
	${MKDIR} -p ${OBJECTDIR}/user/src
	@NMOUTPUT=`${NM} ${OBJECTDIR}/user/src/main.o`; \
	if (echo "$$NMOUTPUT" | ${GREP} '|main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T main$$') || \
	   (echo "$$NMOUTPUT" | ${GREP} 'T _main$$'); \
	then  \
	    ${RM} "$@.d";\
	    $(COMPILE.cc) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c++11  -Dmain=__nomain -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/user/src/main_nomain.o user/src/main.cpp;\
	else  \
	    ${CP} ${OBJECTDIR}/user/src/main.o ${OBJECTDIR}/user/src/main_nomain.o;\
	fi

# Run Test Targets
.test-conf:
	@if [ "${TEST}" = "" ]; \
	then  \
	    ${TESTDIR}/TestFiles/f1 || true; \
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
