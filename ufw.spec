Summary:	Uncomplicated Firewall
Name:		ufw
Version:	0.30.1
Release:	1
License:	GPL v3+
Group:		Networking/Admin
URL:		http://launchpad.net/ufw
Source0:	http://launchpad.net/ufw/0.30/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	3182fad2249cf5f7e5589f44f0f078bd
Patch0:		common.py-file.patch
BuildRequires:	iptables-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Uncomplicated Firewall(ufw) is a front-end for netfilter, which
aims to make it easier for people unfamiliar with firewall concepts.
Ufw provides a framework for managing netfilter as well as
manipulating the firewall.

%prep
%setup -q
# Submited patch through ufw's bug report
# Fix directory locations instead of #CONFIG_PREFIX#
# http://bugs.launchpad.net/ufw/+bug/819600
%patch0 -p0

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYING README* TODO AUTHORS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/default/ufw
%dir %{_sysconfdir}/ufw
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ufw/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ufw/*.rules
%dir %{_sysconfdir}/ufw/applications.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ufw/applications.d/*

%attr(755,root,root) %{_sbindir}/ufw
%{_mandir}/man8/ufw-framework.8*
%{_mandir}/man8/ufw.8*
%{_datadir}/%{name}
%dir /lib/ufw
/lib/ufw/ufw-init
/lib/ufw/ufw-init-functions
/lib/ufw/user.rules
/lib/ufw/user6.rules
%{py_sitescriptdir}/ufw
%{py_sitescriptdir}/ufw-%{version}-py*.egg-info
