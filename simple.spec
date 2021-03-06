%define __prelink_undo_cmd %{nil}
%define installdir %{home}/%{user}/%{name}
%define python /usr/bin/python2.7
%define portbase 13080
%define debug_package %{nil}

Name: %{name}
Version: %{version}
Release: 1
Summary: %{name} website
URL: http://cirb.irisnet.be
License: GPL
Vendor: CIRB-CIBG
Packager: bsuttor <bsuttor@cirb.irisnet.be>
Group: Applications/Database
Buildroot: %{_tmppath}/%{name}-buildroot
Source: %{name}-%{version}.tar.gz
BuildRequires:  git, zlib-devel, freetype-devel, libjpeg-devel, gcc
BuildRequires:  libxslt-devel
AutoReqProv: no

%description
%{summary}

%package    core
Summary:    %{summary} - core without any clients
Group: Applications/Database
Requires:   openssl-devel
Requires:   python27-devel
Requires:   zlib freetype
AutoReqProv: no
%description core
%{summary}

%package    zeoserver
Summary:    %{summary} - core
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description zeoserver
%{summary}

%package    client1
Summary:    %{summary} - client1
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description client1
%{summary}

%package    client2
Summary:    %{summary} - client2
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description client2
%{summary}

%package    client3
Summary:    %{summary} - client3
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description client3
%{summary}

%package    client4
Summary:    %{summary} - client4
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description client4
%{summary}

%prep
%setup

%build
# BUILD
# Buildout cannot be run into RPM_BUILD_ROOT
# RPM_BUILD_ROOT is deleted by install macro
BUILDOUT_DIR=$RPM_BUILD_DIR/buildout
%{run_buildout} %{python} $RPM_BUILD_DIR/%{name}-%{version} $BUILDOUT_DIR rpm.cfg %{buildout_version} %{setuptools_version}

%install
# BUILDROOT
BUILDOUT_DIR=$RPM_BUILD_DIR/buildout
TARGET_DIR=%{installdir}
%{install_buildout} $BUILDOUT_DIR $TARGET_DIR $RPM_BUILD_ROOT

%files core
%defattr(-, %{user}, %{user}, 0755)
%{installdir}/eggs
%{installdir}/var/log
%dir %{installdir}/bin
%dir %{installdir}/parts
%dir %{installdir}/var
%dir %{installdir}/etc

%pre core
exit 0


%post core
/sbin/ldconfig

%preun core
find %{installdir} -name "*.pyc" -delete;
find %{installdir} -name "*.pyo" -delete;
find %{installdir} -name "*.mo" -delete;

%postun core
/sbin/ldconfig

%files zeoserver
%defattr(-, %{user}, %{user} , 0755)
%{installdir}/parts/zeoserver/etc/zeo.conf
#%{installdir}/bin/zodbpack
%{installdir}/bin/backup
%{installdir}/bin/restore
%{installdir}/bin/snapshotbackup
%{installdir}/bin/snapshotrestore
%{installdir}/bin/fullbackup
%{installdir}/bin/repozo
%{installdir}/bin/zeopack
%{installdir}/bin/zeoserver
%{installdir}/parts/zeoserver
%{installdir}/var/zeoserver
%{installdir}/var/filestorage
%{installdir}/var/blobstorage

%files client1
%defattr(-, %{user}, %{user}, 0755)
%{installdir}/parts/client1/etc/zope.conf
%{installdir}/bin/client1
%{installdir}/parts/client1
%{installdir}/var/client1

%files client2
%defattr(-, %{user}, %{user}, 0755)
%{installdir}/parts/client2/etc/zope.conf
%{installdir}/bin/client2
%{installdir}/parts/client2
%{installdir}/var/client2

%files client3
%defattr(-, %{user}, %{user}, 0755)
%{installdir}/parts/client3/etc/zope.conf
%{installdir}/bin/client3
%{installdir}/parts/client3
%{installdir}/var/client3

%files client4
%defattr(-, %{user}, %{user}, 0755)
%{installdir}/parts/client4/etc/zope.conf
%{installdir}/bin/client4
%{installdir}/parts/client4
%{installdir}/var/client4


%clean
rm -rf $INSTALL_DIR $RPM_BUILD_ROOT/etc $RPM_BUILD_DIR%{installdir}
#echo NOOP

%changelog
* Thu Jun 07 2013 - Benoît Suttor <bsuttor@cirb.irisnet.be>
- Use python2.7
- Use, like tracis-ci, unified installer for downloading eggs.
* Thu May 14 2013 - Benoît Suttor <bsuttor@cirb.irisnet.be>
- Replace backup files (from recipe)
- Add fullbackup script
* Thu Dec 20 2012 - Benoît Suttor <bsuttor@cirb.irisnet.be> 0.1.3
- Add client3 and client4, and no replace backup files
* Tue Oct 2 2012 -  Godefroid Chapelle <gotcha@bubblenet.be> 0.1.2
- Use 'name' instead of 'portal' as input parameter
- Add etc/ in install_dir
- Do not distribute develop-eggs
* Wed Jul 25 2012 -  Benoît Suttor <bsuttor@cirb.irisnet.be> 0.1.1
- Add client2 construction
- Clean path into zope.conf file and zeo.conf file
* Tue Jul 10 2012 - Benoît Suttor <bsuttor@cirb.irisnet.be> 0.1
- initial build
