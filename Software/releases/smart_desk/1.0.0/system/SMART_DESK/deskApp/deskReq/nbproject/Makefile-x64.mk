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
	${OBJECTDIR}/_ext/59aedd0e/DeskRequester.o \
	${OBJECTDIR}/_ext/aa91408b/main.o \
	${OBJECTDIR}/_ext/aff35550/AutonomousCommFrame.o \
	${OBJECTDIR}/_ext/c6fb8ee4/ZmqRequester.o \
	${OBJECTDIR}/_ext/c6fb8ee4/iZmq.o


# C Compiler Flags
CFLAGS=-m64

# CC Compiler Flags
CCFLAGS=-m64
CXXFLAGS=-m64

# Fortran Compiler Flags
FFLAGS=-m64

# Assembler Flags
ASFLAGS=--64

# Link Libraries and Options
LDLIBSOPTIONS=-lpthread `pkg-config --libs libzmq`  

# Build Targets
.build-conf: ${BUILD_SUBPROJECTS}
	"${MAKE}"  -f nbproject/Makefile-${CND_CONF}.mk user/x64/deskreq

user/x64/deskreq: ${OBJECTFILES}
	${MKDIR} -p user/x64
	g++ -o user/x64/deskreq ${OBJECTFILES} ${LDLIBSOPTIONS}

${OBJECTDIR}/_ext/59aedd0e/DeskRequester.o: ../../../../../ws/Linux/myLib/Library/src/Smartdesk/DeskRequester.cpp
	${MKDIR} -p ${OBJECTDIR}/_ext/59aedd0e
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c++11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/59aedd0e/DeskRequester.o ../../../../../ws/Linux/myLib/Library/src/Smartdesk/DeskRequester.cpp

${OBJECTDIR}/_ext/aa91408b/main.o: /home/thanh/aos/system/SMART_DESK/deskApp/deskReq/main.cpp
	${MKDIR} -p ${OBJECTDIR}/_ext/aa91408b
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c++11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/aa91408b/main.o /home/thanh/aos/system/SMART_DESK/deskApp/deskReq/main.cpp

${OBJECTDIR}/_ext/aff35550/AutonomousCommFrame.o: /home/thanh/ws/Linux/myLib/Library/src/Device/AutonomousCommFrame.c
	${MKDIR} -p ${OBJECTDIR}/_ext/aff35550
	${RM} "$@.d"
	$(COMPILE.c) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/aff35550/AutonomousCommFrame.o /home/thanh/ws/Linux/myLib/Library/src/Device/AutonomousCommFrame.c

${OBJECTDIR}/_ext/c6fb8ee4/ZmqRequester.o: /home/thanh/ws/Linux/myLib/Library/src/ZMQ/ZmqRequester.cpp
	${MKDIR} -p ${OBJECTDIR}/_ext/c6fb8ee4
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c++11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/c6fb8ee4/ZmqRequester.o /home/thanh/ws/Linux/myLib/Library/src/ZMQ/ZmqRequester.cpp

${OBJECTDIR}/_ext/c6fb8ee4/iZmq.o: /home/thanh/ws/Linux/myLib/Library/src/ZMQ/iZmq.cpp
	${MKDIR} -p ${OBJECTDIR}/_ext/c6fb8ee4
	${RM} "$@.d"
	$(COMPILE.cc) -g -Iuser/inc -I/home/thanh/ws/Linux/myLib/Library/inc `pkg-config --cflags libzmq` -std=c++11  -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/c6fb8ee4/iZmq.o /home/thanh/ws/Linux/myLib/Library/src/ZMQ/iZmq.cpp

# Subprojects
.build-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r ${CND_BUILDDIR}/${CND_CONF}

# Subprojects
.clean-subprojects:

# Enable dependency checking
.dep.inc: .depcheck-impl

include .dep.inc
