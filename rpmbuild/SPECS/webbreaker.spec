%global user webbreaker
%global installdir /opt/webbreaker
%global allocated_id 666
%define build_timestamp %(date +"%m-%d-%Y")
%define _topdir %(pwd)/

Summary:    Client for Dynamic Application Security Test Orchestration (DASTO).
Name:       webbreaker
Version:    2.0
Release:    03%{?dist}
Source0:    %{name}-%{version}.tar.gz
Group:      Security Tools
License:    MIT
Requires:   shadow-utils, cronie, crontabs, glibc
Requires:   /bin/rm, /usr/sbin/useradd, /usr/sbin/groupadd, /bin/ln, /usr/sbin/alternatives, /bin/sed, /usr/bin/getent, /usr/sbin/userdel
Packager:   Brandon Spruth <brandon.spruth2@target.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:     %{_prefix}
BuildArch:  x86_64
Vendor:     Target Brands, Inc.
URL:        https://github.com/target/webbreaker

%description
WebBreaker is an open source Dynamic Application Security Test Orchestration (DASTO) client, enabling development teams to release secure software with continuous delivery, visibility, and scalability.

%prep
%setup -q -n %{name}-%{version}

%pre
# Add the webbreaker user and group
getent group %{user} >/dev/null || groupadd -f -g %{allocated_id} -r %{user}
if ! getent passwd %{user} >/dev/null ; then
    if ! getent passwd %{allocated_id} >/dev/null ; then
      useradd -r -u %{allocated_id} -g %{user} -d %{installdir} -s /bin/sh -c "WebBreaker Client User" %{user}
    else
      useradd -r -g %{user} -d %{installdir} -s /bin/sh -c "WebBreaker User for DASTO" %{user}
    fi
fi
exit 0

#make sure no old log or pid files are here
rm -rf $RPM_BUILD_ROOT%{installdir}/log/*

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{installdir}
install -d $RPM_BUILD_ROOT%{installdir}
cp opt/webbreaker/webbreaker-cli $RPM_BUILD_ROOT/opt/webbreaker/webbreaker-cli

%post
/usr/bin/chown -R %{user}:%{user} %{installdir} 2> /dev/null

/usr/sbin/alternatives --install /usr/bin/webbreaker webbreaker %{installdir}/webbreaker-cli 100
/usr/sbin/alternatives --auto webbreaker
/usr/sbin/alternatives --set webbreaker %{installdir}/webbreaker-cli

%preun

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,%{user},%{user},755)
%attr(755,%{user},%{user}) %dir %{installdir}
%attr(755,%{user},%{user}) %{installdir}/webbreaker-cli

%changelog
* Fri Dec 1 2017 Target Product Security Engineering <brandon.spruth2@target.com> - 2.0-03
- Added Webinspect proxy functionality.

* Tue Nov 28 2017 Target Product Security Engineering <brandon.spruth2@target.com> - 2.0-04
- Refactored to just webinspect-cli binary

* Wed Nov 22 2017 Target Product Security Engineering <brandon.spruth2@target.com> - 2.0-01
- Initial creation
