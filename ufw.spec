Summary:	Uncomplicated Firewall
Name:		ufw
Version:	0.35
Release:	1
License:	GPL v3+
Group:		Networking/Admin
Source0:	http://launchpad.net/ufw/%{version}/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	b7cd2dd4e4e98e46df125fee06edff92
Patch0:		sysconfig.patch
Patch1:		dont-check-iptables.patch
URL:		http://launchpad.net/ufw
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
Requires:	iptables >= 1.4.16
Requires:	iptables-init
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Uncomplicated Firewall(ufw) is a front-end for netfilter, which
aims to make it easier for people unfamiliar with firewall concepts.
Ufw provides a framework for managing netfilter as well as
manipulating the firewall.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%{__sed} -i -re 's,#! /usr/bin/env ,#!,' setup.py

# typo
%{__sed} -i -e 's,/etc/defaults/ufw,/etc/sysconfig/ufw,' README

# pldize sysconfig path
grep -rl /etc/default/ufw . | xargs %{__sed} -i -e 's,/etc/default/ufw,/etc/sysconfig/ufw,'

%build
# We skip 'build' and run 'install' directly
# http://bugs.launchpad.net/ufw/+bug/819600
#%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%py_install
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README* TODO AUTHORS
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ufw
%dir %{_sysconfdir}/ufw
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ufw/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ufw/*.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ufw/after.init
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ufw/before.init
%dir %{_sysconfdir}/ufw/applications.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ufw/applications.d/*

%attr(755,root,root) %{_sbindir}/ufw
%{_mandir}/man8/ufw-framework.8*
%{_mandir}/man8/ufw.8*
%{_datadir}/%{name}
%dir /lib/ufw
%attr(755,root,root) /lib/ufw/ufw-init
/lib/ufw/ufw-init-functions
%dir %{py_sitescriptdir}/ufw
%{py_sitescriptdir}/ufw/*.py[co]
%{py_sitescriptdir}/ufw-%{version}-py*.egg-info
