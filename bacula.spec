%define _libexecdir /usr/libexec
%define uid 133
%define username bacula
%define _guiver 7.0.2
%define group Archiving/Backup

%define with_omv 1

Name:               bacula
Version:            7.0.2
Release:            1
Summary:            Cross platform network backup for Linux, Unix, Mac and Windows
License:            AGPLv3 
Group:              %{group}
URL:                http://www.bacula.org
# this shit will be fixed by who epoched the previouse build
Epoch:		        2
Source0:            http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	    bacula.rpmlintrc
Source2:            quickstart_postgresql.txt
Source3:            quickstart_mysql.txt
Source4:            quickstart_sqlite3.txt
Source5:            README
Source6:            %{name}.logrotate
Source7:            %{name}-fd.init
Source8:            %{name}-dir.init
Source9:            %{name}-sd.init
Source10:           %{name}-fd.service
Source11:           %{name}-dir.service
Source12:           %{name}-sd.service
Source13:           %{name}-bat.desktop
Source14:           %{name}-traymonitor.desktop
Source15:           %{name}-fd.sysconfig
Source16:           %{name}-dir.sysconfig
Source17:           %{name}-sd.sysconfig


Patch1:             %{name}-5.0.2-openssl.patch
Patch2:             %{name}-7.0.0-queryfile.patch
Patch3:             %{name}-5.0.3-sqlite-priv.patch
Patch4:             %{name}-5.2.13-bat-build.patch
Patch5:             %{name}-5.2.12-seg-fault.patch
Patch6:             %{name}-5.2.13-logwatch.patch
Patch7:             %{name}-non-free-code.patch
Patch8:             %{name}-7.0.2-configure.patch
Patch9:             %{name}-7.0.2-git.patch

BuildRequires:      desktop-file-utils
BuildRequires:      perl
BuildRequires:      sed

BuildRequires:      glibc-devel
BuildRequires:      acl-devel
BuildRequires:      stdc++-devel
BuildRequires:      pkgconfig(libxml-2.0)
BuildRequires:      cap-devel
BuildRequires:      liblzo-devel

%if %{with_omv} 
BuildRequires:      mariadb-devel >= 3.23
%else
BuildRequires:      mysql-devel
%endif
BuildRequires:      pkgconfig(libecpg)
BuildRequires:      pkgconfig(sqlite3)
BuildRequires:      pkgconfig(ncurses)
BuildRequires:      pkgconfig(openssl)
BuildRequires:      readline-devel
BuildRequires:      pkgconfig(zlib)
BuildRequires:      qt4-devel >= 4.6.2
BuildRequires:      tcp_wrappers-devel
BuildRequires:      systemd


%description
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture and is efficient and relatively easy to
use, while offering many advanced storage management features that make it easy
to find and recover lost or damaged files.


##########################################
%define baculalibname %mklibname bacula %{_guiver}

%package -n %{baculalibname}
Summary:            Bacula libraries
Group:              %{group}


%description -n %{baculalibname}
Bacula is a set of programs that allow you to manage the backup,
recovery, and verification of computer data across a network of
different computers. It is based on a client/server architecture.

This package contains basic Bacula libraries, which are used by all
Bacula programs.

%files  -n %{baculalibname}
%doc AUTHORS ChangeLog LICENSE SUPPORT ReleaseNotes
%{_libdir}/libbac-%{version}.so
%{_libdir}/libbaccfg-%{version}.so
%{_libdir}/libbacfind-%{version}.so


############################################
%define devname		%mklibname -d %{name}

%package  -n	%{devname}
Summary:            Bacula development files
Group:              Development/Other
Requires:           %{baculalibname} = %{EVRD}
Requires:           bacula-dir-sql = %{EVRD}

%description  -n	%{devname}
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This development package contains static libraries and header files.

%files   -n	%{devname}
%{_includedir}/bacula
%{_libdir}/libbac.so
%{_libdir}/libbaccfg.so
%{_libdir}/libbacfind.so
%{_libdir}/libbacsql.so

##############################################

%package dir-sql
Summary:            Bacula SQL libraries
Group:              %{group}
# I don't know if still neded to be checked
%if %{with_omv}
Requires:	mariadb-client
Suggests:	mariadb
%endif
Obsoletes:          bacula-dir-mysql <= 5.0.13
Obsoletes:          bacula-dir-sqlite3 <= 5.0.13
Obsoletes:          bacula-dir-pgsql <= 5.0.13

Provides:           bacula-dir-mysql = %{EVRD}
Provides:           bacula-dir-sqlite3 = %{EVRD}
Provides:           bacula-dir-postgresql = %{EVRD}

%description dir-sql
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the SQL Bacula libraries, which are used by Director and
Storage daemons. You have to select your preferred catalog library through the
alternatives system.

%files dir-sql
%{_libdir}/libbaccats-mysql-%{version}.so
%{_libdir}/libbaccats-mysql.so
%{_libdir}/libbaccats-postgresql-%{version}.so
%{_libdir}/libbaccats-postgresql.so
%{_libdir}/libbaccats-sqlite3-%{version}.so
%{_libdir}/libbaccats-sqlite3.so
%{_libdir}/libbacsql-%{version}.so
%{_libdir}/libbaccats-%{version}.so
##############################################

%package common
Summary:            Common Bacula files
Group:              %{group}
Provides:           group(%username) = %uid
Provides:           user(%username) = %uid
Provides:           bacula-common = %{EVRD}

Requires:           %{baculalibname} = %{EVRD}
Requires(pre):      shadow-utils
Requires(postun):   shadow-utils

%description common
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains files common to all Bacula daemons.

%files common
%doc README quickstart_*
%config(noreplace) %{_sysconfdir}/logrotate.d/bacula
%dir %{_localstatedir}/log/bacula %attr(750, bacula, bacula)
%dir %{_localstatedir}/spool/bacula %attr(750, bacula, bacula)
%dir %{_libexecdir}/%{name}
%dir %{_sysconfdir}/%{name} %attr(755,root,root)
%{_libexecdir}/%{name}/btraceback.dbx
%{_libexecdir}/%{name}/btraceback.gdb
%{_libexecdir}/%{name}/bacula_config
%{_libexecdir}/%{name}/btraceback.mdb
%{_mandir}/man8/btraceback.8*
%{_mandir}/man8/bpluginfo.8*
%{_sbindir}/btraceback
%{_sbindir}/bpluginfo
#############################################

%package client
Summary:            Bacula backup client
Group:              %{group}
Requires:           bacula-common = %{EVRD}
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd


%description client
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the bacula client, the daemon running on the system to be
backed up.

%files client
%config(noreplace) %{_sysconfdir}/bacula/bacula-fd.conf %attr(640,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/bacula-fd
%{_mandir}/man8/bacula-fd.8*
%{_libdir}/bacula/bpipe-fd.so
%{_sbindir}/bacula-fd
%{_unitdir}/bacula-fd.service

###############################################
%package dir-common
Summary:            Bacula Director files
Group:              %{group}
Requires:           bacula-common = %{EVRD}
Requires:           %{baculalibname} = %{EVRD}
Requires:           bacula-dir-sql = %{EVRD}
Requires:           logwatch
# Director backends merged into core.
Provides:           bacula-dir-common = %{EVRD}
Obsoletes:          bacula-dir-common < 5.2.13
Provides:           bacula-dir-mysql = %{EVRD}
Obsoletes:          bacula-dir-mysql < 5.2.13
Provides:           bacula-dir-sqlite3 = %{EVRD}
Obsoletes:          bacula-dir-sqlite3 < 5.2.13
Provides:           bacula-dir-pgsql = %{EVRD}
Obsoletes:          bacula-dir-pgsql < 5.2.13

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd


%description dir-common
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the director files.

%files dir-common
%doc updatedb examples/sample-query.sql
%config(noreplace) %{_sysconfdir}/bacula/bacula-dir.conf %attr(640,root,bacula)
%config(noreplace) %{_sysconfdir}/bacula/query.sql %attr(640,root,bacula)
%config(noreplace) %{_sysconfdir}/logwatch/conf/logfiles/bacula.conf
%config(noreplace) %{_sysconfdir}/logwatch/conf/services/bacula.conf
%config(noreplace) %{_sysconfdir}/sysconfig/bacula-dir
%{_libexecdir}/%{name}/create_bacula_database
%{_libexecdir}/%{name}/delete_catalog_backup
%{_libexecdir}/%{name}/drop_bacula_database
%{_libexecdir}/%{name}/drop_bacula_tables
%{_libexecdir}/%{name}/grant_bacula_privileges
%{_libexecdir}/%{name}/make_bacula_tables
%{_libexecdir}/%{name}/make_catalog_backup.pl
%{_libexecdir}/%{name}/update_bacula_tables
%{_libexecdir}/%{name}/create_mysql_database
%{_libexecdir}/%{name}/drop_mysql_database
%{_libexecdir}/%{name}/drop_mysql_tables
%{_libexecdir}/%{name}/grant_mysql_privileges
%{_libexecdir}/%{name}/make_mysql_tables
%{_libexecdir}/%{name}/update_mysql_tables
%{_libexecdir}/%{name}/create_sqlite3_database
%{_libexecdir}/%{name}/drop_sqlite3_database
%{_libexecdir}/%{name}/drop_sqlite3_tables
%{_libexecdir}/%{name}/grant_sqlite3_privileges
%{_libexecdir}/%{name}/make_sqlite3_tables
%{_libexecdir}/%{name}/update_sqlite3_tables
%{_libexecdir}/%{name}/create_postgresql_database
%{_libexecdir}/%{name}/drop_postgresql_database
%{_libexecdir}/%{name}/drop_postgresql_tables
%{_libexecdir}/%{name}/grant_postgresql_privileges
%{_libexecdir}/%{name}/make_postgresql_tables
%{_libexecdir}/%{name}/update_postgresql_tables
%{_mandir}/man1/bsmtp.1*
%{_mandir}/man8/bacula-dir.8*
%{_mandir}/man8/bregex.8*
%{_mandir}/man8/bwild.8*
%{_mandir}/man8/dbcheck.8*
%{_sbindir}/bacula-dir
%{_sbindir}/bregex
%{_sbindir}/bsmtp
%{_sbindir}/bwild
%{_sbindir}/dbcheck
%{_sysconfdir}/logwatch/scripts/services/bacula
%{_sysconfdir}/logwatch/scripts/shared/applybaculadate
%{_unitdir}/bacula-dir.service

#############################################
%package sd
Summary:            Bacula storage daemon files
Group:              %{group}
Requires:           bacula-common = %{EVRD}
Requires:           %{baculalibname} = %{EVRD}
Requires:           bacula-dir-sql = %{EVRD}
Requires:           mt-st
Provides:           bacula-storage-common = %{EVRD}
Provides:           bacula-storage-mysql = %{EVRD}
Provides:           bacula-storage-sqlite3 = %{EVRD}
Provides:           bacula-storage-pgsql = %{EVRD}

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd


%description sd
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the storage daemon, the daemon responsible for writing
the data received from the clients onto tape drives or other mass storage
devices.

%files sd
%config(noreplace) %{_sysconfdir}/bacula/bacula-sd.conf %attr(640,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/bacula-sd
%{_libexecdir}/%{name}/disk-changer
%{_libexecdir}/%{name}/dvd-handler
%{_libexecdir}/%{name}/mtx-changer
%{_libexecdir}/%{name}/mtx-changer.conf
%{_mandir}/man8/bacula-sd.8*
%{_mandir}/man8/bcopy.8*
%{_mandir}/man8/bextract.8*
%{_mandir}/man8/bls.8*
%{_mandir}/man8/bscan.8*
%{_mandir}/man8/btape.8*
%{_sbindir}/bacula-sd
%{_sbindir}/bcopy
%{_sbindir}/bextract
%{_sbindir}/bls
%{_sbindir}/bscan
%{_sbindir}/btape
%{_unitdir}/bacula-sd.service

##############################################


%package console
Summary:            Bacula management console
Group:              %{group}
Obsoletes:          bacula-console-wx <= 5.0.13
Requires:           %{baculalibname} = %{EVRD}

%description console
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the command-line management console for the bacula backup
system.

%files console
%config(noreplace) %{_sysconfdir}/bacula/bconsole.conf %attr(640,root,root)
%{_mandir}/man8/bconsole.8*
%{_sbindir}/bconsole

##################################################

%package bat
Summary:            Bacula bat console
Group:              %{group}
Requires:           %{baculalibname} = %{EVRD}

%description bat
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the bat version of the bacula management console.

%files bat
%config(noreplace) %{_sysconfdir}/bacula/bat.conf %attr(640,root,root)
%{_datadir}/applications/bacula-bat.desktop
%{_datadir}/bacula/*.html
%{_datadir}/bacula/*.png
%{_datadir}/pixmaps/bat.png
%{_mandir}/man1/bat.1*
%{_sbindir}/bat

############################################

%package tray-monitor
Summary:            Bacula system tray monitor
Group:              %{group}
Requires:           %{baculalibname} = %{EVRD}

%description tray-monitor
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the Gnome and KDE compatible tray monitor to monitor your
bacula server.

%files tray-monitor
%config(noreplace) %{_sysconfdir}/bacula/tray-monitor.conf %attr(640,root,root)
%{_datadir}/applications/bacula-traymonitor.desktop
%{_datadir}/pixmaps/bacula-tray-monitor.png
%{_mandir}/man1/bacula-tray-monitor.1*
%{_sbindir}/bacula-tray-monitor

#################################################
# missing nagios in omv
# enabled bacula plugin in nagios-check

#%package -n nagios-check_bacula
#Summary:            Nagios Plugin - check_bacula
#Group:              %{group}
#Requires:           %{baculalibname} = %{version}-%{release}
#Requires:           nagios

#%description -n nagios-check_bacula
#Provides check_bacula support for Nagios.

#%files -n nagios-check_bacula
#%{_libdir}/nagios/plugins/check_bacula

###################################################
%prep
%setup -q
%patch1 -p2
%patch2 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p2
cp %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} .

# Remove execution permissions from files we're packaging as docs later on
find updatedb -type f | xargs chmod -x

%build
build() {
export LDFLAGS="$LDFLAGS -lreadline -lncurses"
export CFLAGS="%{optflags} -I%{_includedir}/ncurses"
export CPPFLAGS="%{optflags} -I%{_includedir}/ncurses"
%configure \
        --disable-conio \
        --disable-rpath \
        --docdir=%{_datadir}/bacula \
        --enable-batch-insert \
        --enable-build-dird \
        --enable-build-stored \
        --enable-includes \
        --enable-largefile \
        --enable-readline \
        --enable-smartalloc \
        --sysconfdir=%{_sysconfdir}/bacula \
        --with-basename=bacula \
        --with-bsrdir=%{_localstatedir}/spool/bacula \
        --with-dir-password=@@DIR_PASSWORD@@ \
        --with-fd-password=@@FD_PASSWORD@@ \
        --with-hostname=localhost \
        --with-logdir=%{_localstatedir}/log/bacula \
        --with-mon-dir-password=@@MON_DIR_PASSWORD@@ \
        --with-mon-fd-password=@@MON_FD_PASSWORD@@ \
        --with-mon-sd-password=@@MON_SD_PASSWORD@@ \
        --with-mysql \
        --with-openssl \
        --with-pid-dir=%{_localstatedir}/run \
        --with-plugindir=%{_libdir}/bacula \
        --with-postgresql \
        --with-scriptdir=%{_libexecdir}/bacula \
        --with-sd-password=@@SD_PASSWORD@@ \
        --with-smtp-host=localhost \
        --with-sqlite3 \
        --with-subsys-dir=%{_localstatedir}/lock/subsys \
        --with-tcp-wrappers \
        --with-working-dir=%{_localstatedir}/spool/bacula \
        --with-x \
        $*
}


export QMAKE=/usr/lib/qt4/bin/qmake
build --enable-bat

# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{make} 
make -C examples/nagios/check_bacula

pushd src/qt-console/tray-monitor
    $QMAKE tray-monitor.pro
    %make
popd


%install
%{makeinstall_std}

# Nagios plugin
#install -p -m 755 -D examples/nagios/check_bacula/.libs/check_bacula %{buildroot}%{_libdir}/nagios/plugins/check_bacula

# Remove catalogue backend symlinks
rm -f %{buildroot}%{_libdir}/libbaccats.so
rm -f %{buildroot}%{_libdir}/libbaccats-%{version}.so

# Bat
install -p -m 644 -D src/qt-console/images/bat_icon.png %{buildroot}%{_datadir}/pixmaps/bat.png
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE13}

# QT Tray monitor
install -p -m 755 -D src/qt-console/tray-monitor/bacula-tray-monitor %{buildroot}%{_sbindir}/bacula-tray-monitor
install -p -m 644 -D src/qt-console/tray-monitor/tray-monitor.conf %{buildroot}%{_sysconfdir}/bacula/tray-monitor.conf
install -p -m 644 -D src/qt-console/images/bat_icon.png %{buildroot}%{_datadir}/pixmaps/bacula-tray-monitor.png
install -p -m 644 -D manpages/bacula-tray-monitor.1 %{buildroot}%{_mandir}/man1/bacula-tray-monitor.1
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE14}

# Logrotate
mkdir -p %{buildroot}%{_localstatedir}/log/bacula
install -p -m 644 -D %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/bacula

# Logwatch
install -p -m 755 -D scripts/logwatch/bacula %{buildroot}%{_sysconfdir}/logwatch/scripts/services/bacula
install -p -m 755 -D scripts/logwatch/applybaculadate %{buildroot}%{_sysconfdir}/logwatch/scripts/shared/applybaculadate
install -p -m 644 -D scripts/logwatch/logfile.bacula.conf %{buildroot}%{_sysconfdir}/logwatch/conf/logfiles/bacula.conf
install -p -m 644 -D scripts/logwatch/services.bacula.conf %{buildroot}%{_sysconfdir}/logwatch/conf/services/bacula.conf

# Systemd unit files
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 -D %{SOURCE10} %{buildroot}%{_unitdir}/bacula-fd.service
install -p -m 644 -D %{SOURCE11} %{buildroot}%{_unitdir}/bacula-dir.service
install -p -m 644 -D %{SOURCE12} %{buildroot}%{_unitdir}/bacula-sd.service



# Sysconfig
install -p -m 644 -D %{SOURCE15} %{buildroot}%{_sysconfdir}/sysconfig/bacula-fd
install -p -m 644 -D %{SOURCE16} %{buildroot}%{_sysconfdir}/sysconfig/bacula-dir
install -p -m 644 -D %{SOURCE17} %{buildroot}%{_sysconfdir}/sysconfig/bacula-sd


# bacula Spool dir
mkdir -p %{buildroot}%{_localstatedir}/spool/bacula

# Clean
rm -f %{buildroot}%{_libexecdir}/bacula/{bacula,bacula-ctl-*,startmysql,stopmysql,bconsole,make_catalog_backup}
rm -f %{buildroot}%{_sbindir}/bacula
rm -f %{buildroot}%{_mandir}/man8/bacula.8.gz
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_datadir}/bacula/{ChangeLog,INSTALL,LICENSE,README,ReleaseNotes,VERIFYING,technotes}

# make rpmlint a happy 
chmod 755 %{buildroot}%{_sbindir}/*
chmod 755 %{buildroot}%{_libdir}/bacula/*
chmod 755 %{buildroot}%{_libexecdir}/bacula/*
chmod 644 %{buildroot}%{_libexecdir}/bacula/btraceback.*


%post dir-sql
/usr/sbin/alternatives --install %{_libdir}/libbaccats.so libbaccats.so %{_libdir}/libbaccats-mysql.so 50
/usr/sbin/alternatives --install %{_libdir}/libbaccats.so libbaccats.so %{_libdir}/libbaccats-sqlite3.so 40
/usr/sbin/alternatives --install %{_libdir}/libbaccats.so libbaccats.so %{_libdir}/libbaccats-postgresql.so 60
# Fix for automatic selection of backends during upgrades
if readlink /etc/alternatives/libbaccats.so | grep --silent mysql || \
   readlink /etc/alternatives/bacula-dir | grep --silent mysql || \
   readlink /etc/alternatives/bacula-sd | grep --silent mysql; then
        /usr/sbin/alternatives --set libbaccats.so %{_libdir}/libbaccats-mysql.so
elif readlink /etc/alternatives/libbaccats.so | grep --silent sqlite || \
   readlink /etc/alternatives/bacula-dir | grep --silent sqlite || \
   readlink /etc/alternatives/bacula-sd | grep --silent sqlite; then
        /usr/sbin/alternatives --set libbaccats.so %{_libdir}/libbaccats-sqlite3.so
else
        /usr/sbin/alternatives --set libbaccats.so %{_libdir}/libbaccats-postgresql.so
fi
/sbin/ldconfig

%preun dir-sql
if [ "$1" = 0 ]; then
        /usr/sbin/alternatives --remove libbaccats.so %{_libdir}/libbaccats-mysql.so
        /usr/sbin/alternatives --remove libbaccats.so %{_libdir}/libbaccats-sqlite3.so
        /usr/sbin/alternatives --remove libbaccats.so %{_libdir}/libbaccats-postgresql.so
fi

%postun dir-sql
/sbin/ldconfig
exit 0

%pre common
getent group %username >/dev/null || groupadd -g %uid -r %username &>/dev/null || :
getent passwd %username >/dev/null || useradd -u %uid -r -s /sbin/nologin \
    -d /var/spool/bacula -M -c 'Bacula Backup System' -g %username %username &>/dev/null || :
exit 0


%post client
%systemd_post %{name}-fd.service

%preun client
%systemd_preun %{name}-fd.service

%postun client
%systemd_postun_with_restart %{name}-fd.service

%post dir-common
%systemd_post %{name}-dir.service

%preun dir-common
%systemd_preun %{name}-dir.service

%postun dir-common
%systemd_postun_with_restart %{name}-dir.service

%post sd
%systemd_post %{name}-sd.service

%preun sd
%systemd_preun %{name}-sd.service

%postun sd
%systemd_postun_with_restart %{name}-sd.service

























