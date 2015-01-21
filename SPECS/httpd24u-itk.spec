%global ver 2.4.7-01

Summary:		MPM Itk for Apache HTTP Server
Name:		httpd-itk
Version:		%( echo %ver | tr '-' '.' )
Release:		4%{?dist}
URL:			http://mpm-itk.sesse.net/
License:		ASL 2.0
Group:		System Environment/Daemons
# It still needed as it targedted for EL5 too
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

Source0:		http://mpm-itk.sesse.net/mpm-itk-%{ver}.tar.gz
Source1:		README.Fedora

BuildRequires:	httpd-devel >= 2.4.7
# There no required strict equal httpd version, just not older, because from it
# used only environment, but package provide fully independent binary file.
Requires:		httpd >= 2.4.7

%description
The Apache HTTP Server is a powerful, efficient, and extensible web server.

This package contain mpm-itk which is an MPM (Multi-Processing Module) for the
Apache web server. Mpm-itk allows you to run each of your vhost under a separate
uid and gid — in short, the scripts and configuration files for one vhost no
longer have to be readable for all the other vhosts.

In summary it is Apache module (opposite CGI solutions like suexec), fast and
allow safely use non-thread-aware code software (like many PHP extensions f.e.)

%prep
%setup -q -n mpm-itk-%{ver}

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -m 644 %{SOURCE1} .
install -D .libs/mpm_itk.so %{buildroot}/%{_httpd_moddir}/mod_mpm_itk.so
install -d %{buildroot}/%{_httpd_modconfdir}/

cat > %{buildroot}/%{_httpd_modconfdir}/00-mpm-itk.conf << EOF
# ITK MPM (Multi-Processing Module). Mpm-itk allows you to run each of your
# vhost under a separate uid and gid - in short, the scripts and configuration
# files for one vhost no longer have to be readable for all the other vhosts.
#LoadModule mpm_itk_module modules/mod_mpm_itk.so
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README CHANGES README.Fedora
%{_httpd_moddir}/mod_mpm_itk.so
%config(noreplace) %{_httpd_modconfdir}/00-mpm-itk.conf

%changelog
* Mon Sep 8 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 2.4.7.01-4
- Fix service name in README.Fedora - bz#1133247.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.7.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.7.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Nov 30 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.4.7.01.1
- Owesome! Httpd 2.4.7 pushed. It shoud not require any hack anymore.
- Major update to 2.4.7-01.
- Apache from 2.4 version have modularity structure, so many changes:
	- Mpm may be build without apache source tree!
	- Exclude apache sources, turn mpm-itk tarball into regular source0.
	- So drop all black magic!
	- Instal it as module, retire separate systemd service files and related stuff.
	- Rewrite README.Fedora.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.22-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 18 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.22-7
- Add separate self own systemd service file and update instruction how to use it (bz#804349).

* Thu Mar 8 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.22-5
- Up apr and upr-utils required BR to 1.3 (http://centos.org/modules/newbb/print.php?form=1&topic_id=35915&forum=37&order=ASC&start=0).
	Do not build for El5 untill this requirement will be met.

* Wed Mar 7 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.22-4
- Port pcre patch from httpd.

* Thu Mar 1 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.22-3
- Add source1 - README.Fedora.

* Thu Feb 23 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.22-2
- Some minor fixes due to Fedora Review. Thanks to Nikos Roussos.

* Sat Feb 18 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.22-1
- Version 2.2.22
- Move content fo README.Fedora in separate file instead of store in SPEC.

* Tue Sep 13 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.21-1
- New version

* Sat Sep 10 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.20-1
- Security upstream update

* Wed Jul 6 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.19-1
- Update to 2.2.19 version follow to upstream.
- Drop outdated patch httpd-2.2.0-authnoprov.patch

* Wed Mar 23 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.17-4
- Follow the main httpd package:
	o Drop merged upstream Patch21: httpd-2.2.11-xfsz.patch
	o Update httpd-2.2.11-corelimit.patch and httpd-2.2.11-selinux.patch.

* Sat Oct 30 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.17-3
- Follow upstream new version 2.2.17 - https://admin.fedoraproject.org/updates/httpd-2.2.17-1.fc13.1

* Wed Jul 28 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.16-2
- Update to Apache 2.2.16 version.

* Sun Apr 04 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.15-1
- Initial spec. Based on httpd.spec in Fedora rawhide. Joe Orton has asked
	initially add MPM-ITK support into main httpd package (BUG#479575) -
	he dismiss enhancment request. After that he was asked (with proposed
	patch) to provide httpd-source package he also dismiss it (BUG#597772).
	Pride is a mortal sin. But I can not get it to do something.
	So, instead just base on always current version of Fedora httpd, I have to
	do it again from begining and doubling... I'll try it do as best as
	possible in this situation.
