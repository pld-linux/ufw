Summary:	Uncomplicated Firewall
Name:		ufw
Version:	0.33
Release:	1
License:	GPL v3+
Group:		Networking/Admin
Source0:	http://launchpad.net/ufw/0.33/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	3747b453d76709e5a99da209fc0bb5f5
URL:		http://launchpad.net/ufw
BuildRequires:	iptables >= 1.4
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	iptables >= 1.4
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

%build
# We skip 'build' and run 'install' directly
# http://bugs.launchpad.net/ufw/+bug/819600
#%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README* TODO AUTHORS
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
%attr(755,root,root) /lib/ufw/ufw-init
/lib/ufw/ufw-init-functions
/lib/ufw/user.rules
/lib/ufw/user6.rules
%dir %{py_sitescriptdir}/ufw
%{py_sitescriptdir}/ufw/*.py[co]
%{py_sitescriptdir}/ufw-%{version}-py*.egg-info
