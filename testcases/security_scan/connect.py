#!/usr/bin/python
#
# Copyright (c) 2016 Red Hat
# Luke Hinds (lhinds@redhat.com)
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# 0.1: OpenSCAP paramiko connection functions

import os
import socket
import paramiko

import functest.utils.functest_logger as ft_logger

# Enable below for connection debugging
# paramiko.util.log_to_file('ssh.log')

# add installer IP from env
INSTALLER_IP = os.getenv('INSTALLER_IP')

# Set up logger
logger = ft_logger.Logger("security_scan").getLogger()


class novaManager:
    def __init__(self, *args):
        self.args = args

    def keystonepass(self):
        com = self.args[0]
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(INSTALLER_IP, port=22, username='stack')
        except paramiko.SSHException:
            logger.error("Password is invalid for "
                         "undercloud host: {0}").format(INSTALLER_IP)
        except paramiko.AuthenticationException:
            logger.error("Authentication failed for "
                         "undercloud host: {0}").format(INSTALLER_IP)
        except socket.error:
            logger.error("Socker Connection failed for "
                         "undercloud host: {0}").format(INSTALLER_IP)
        stdin, stdout, stderr = client.exec_command(com)
        return stdout.read()


class connectionManager:
    def __init__(self, host, port, user, user_key, *args):
        self.host = host
        self.port = port
        self.user = user
        self.user_key = user_key
        self.args = args

    def remotescript(self):
        localpath = self.args[0]
        remotepath = self.args[1]
        com = self.args[2]

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connection to undercloud
        try:
            client.connect(INSTALLER_IP, port=22, username='stack')
        except paramiko.SSHException:
            logger.error("Authentication failed for "
                         "host: {0}").format(self.host)
        except paramiko.AuthenticationException:
            logger.error("Authentication failed for "
                         "host: {0}").format(self.host)
        except socket.error:
            logger.error("Socker Connection failed for "
                         "undercloud host: {0}").format(self.host)

        transport = client.get_transport()
        local_addr = ('127.0.0.1', 0)
        channel = transport.open_channel("direct-tcpip",
                                         (self.host, int(self.port)),
                                         (local_addr))
        remote_client = paramiko.SSHClient()
        remote_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Tunnel to overcloud
        try:
            remote_client.connect('127.0.0.1', port=22, username=self.user,
                                  key_filename=self.user_key, sock=channel)
            sftp = remote_client.open_sftp()
            sftp.put(localpath, remotepath)
        except paramiko.SSHException:
            logger.error("Authentication failed for "
                         "host: {0}").format(self.host)
        except paramiko.AuthenticationException:
            logger.error("Authentication failed for "
                         "host: {0}").format(self.host)
        except socket.error:
            logger.error("Socker Connection failed for "
                         "undercloud host: {0}").format(self.host)

        output = ""
        stdin, stdout, stderr = remote_client.exec_command(com)
        stdout = stdout.readlines()
        # remove script
        sftp.remove(remotepath)
        remote_client.close()
        client.close()
        # Pipe back stout
        for line in stdout:
            output = output + line
        if output != "":
            return output

    def remotecmd(self):
        com = self.args[0]

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connection to undercloud
        try:
            client.connect(INSTALLER_IP, port=22, username='stack')
        except paramiko.SSHException:
            logger.error("Authentication failed for "
                         "host: {0}").format(self.host)
        except paramiko.AuthenticationException:
            logger.error("Authentication failed for "
                         "host: {0}").format(self.host)
        except socket.error:
            logger.error("Socker Connection failed for "
                         "undercloud host: {0}").format(self.host)

        transport = client.get_transport()
        local_addr = ('127.0.0.1', 0)  # 0 denotes choose random port
        channel = transport.open_channel("direct-tcpip",
                                         (self.host, int(self.port)),
                                         (local_addr))
        remote_client = paramiko.SSHClient()
        remote_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Tunnel to overcloud
        try:
            remote_client.connect('127.0.0.1', port=22, username=self.user,
                                  key_filename=self.user_key, sock=channel)
        except paramiko.SSHException:
            logger.error("Authentication failed for "
                         "host: {0}").format(self.host)
        except paramiko.AuthenticationException:
            logger.error("Authentication failed for "
                         "host: {0}").format(self.host)
        except socket.error:
            logger.error("Socker Connection failed for "
                         "undercloud host: {0}").format(self.host)

        chan = remote_client.get_transport().open_session()
        chan.get_pty()
        f = chan.makefile()
        chan.exec_command(com)
        print f.read()

        remote_client.close()
        client.close()

    def download_reports(self):
        dl_folder = self.args[0]
        reportfile = self.args[1]
        reportname = self.args[2]
        resultsname = self.args[3]
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connection to overcloud
        try:
            client.connect(INSTALLER_IP, port=22, username='stack')
        except paramiko.SSHException:
            logger.error("Authentication failed for "
                         "host: {0}").format(self.host)
        except paramiko.AuthenticationException:
            logger.error("Authentication failed for "
                         "host: {0}").format(self.host)
        except socket.error:
            logger.error("Socker Connection failed for "
                         "undercloud host: {0}").format(self.host)

        transport = client.get_transport()
        local_addr = ('127.0.0.1', 0)  # 0 denotes choose random port
        channel = transport.open_channel("direct-tcpip",
                                         (self.host, int(self.port)),
                                         (local_addr))
        remote_client = paramiko.SSHClient()
        remote_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Tunnel to overcloud
        try:
            remote_client.connect('127.0.0.1', port=22, username=self.user,
                                  key_filename=self.user_key, sock=channel)
        except paramiko.SSHException:
            logger.error("Authentication failed for "
                         "host: {0}").format(self.host)
        except paramiko.AuthenticationException:
            logger.error("Authentication failed for "
                         "host: {0}").format(self.host)
        except socket.error:
            logger.error("Socker Connection failed for "
                         "undercloud host: {0}").format(self.host)
        # Download the reports
        sftp = remote_client.open_sftp()
        logger.info('Downloading \"{0}\"...\n').format(reportname)
        sftp.get(reportfile, ('{0}/{1}'.format(dl_folder, reportname)))
        logger.info('Downloading \"{0}\"...\n').format(resultsname)
        sftp.get(reportfile, ('{0}/{1}'.format(dl_folder, resultsname)))
        sftp.close()
        transport.close()
