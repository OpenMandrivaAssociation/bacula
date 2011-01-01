# required to build 3.0.0 correctly
# those two are required to build on 2009.1+
%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed 1

%define _disable_libtoolize 1

%define name bacula

%define _guiver 5.0.2

%define _cur_db_ver 12

# (eugeni) starting with 5.0.0, bacula dropped sqlite2 support
# in order to be able to compile everything in one run, sqlite3 support
# became mandatory now
%define MYSQL 1
%define PGSQL 1
%define WXWINDOWS 1
%define BAT 1
%define TCPW 1
%define GUI 1
%define TRAY 1

# directories and paths
%define sysconf_dir %{_sysconfdir}/bacula
%define script_dir %{_libdir}/bacula
%define working_dir /var/lib/bacula
%define archivedir /var/spool/bacula
%define subsysdir /var/lock/subsys

%{?_with_mysql: %{expand: %%global MYSQL 1}}
%{?_without_mysql: %{expand: %%global MYSQL 0}}
%{?_with_pgsql: %{expand: %%global PGSQL 1}}
%{?_without_pgsql: %{expand: %%global PGSQL 0}}
%{?_with_wx: %{expand: %%global WXWINDOWS 1}}
%{?_without_wx: %{expand: %%global WXWINDOWS 0}}
%{?_with_bat: %{expand: %%global BAT 1}}
%{?_without_bat: %{expand: %%global BAT 0}}
%{?_with_wrap: %{expand: %%global TCPW 1}}
%{?_without_wrap: %{expand: %%global TCPW 0}}
%{?_with_gui: %{expand: %%global GUI 1}}
%{?_without_gui: %{expand: %%global GUI 0}}
%{?_with_tray: %{expand: %%global TRAY 1}}
%{?_without_tray: %{expand: %%global TRAY 0}}

%if %mdkversion <= 200700
%define BAT 0
%define TRAY 0
%endif

%define blurb Bacula - It comes by night and sucks the vital essence from your computers.

# fixes passwords in configuration files
# removing "SubSys Directory" is needed if upgrading from 1.30a or lower
%define post_fix_config() { umask 0037; if [ -s %{sysconf_dir}/.pw.sed ]; then for i in %{sysconf_dir}/%{1}.conf %{sysconf_dir}/%{1}.conf.rpmnew; do if [ -s $i ]; then sed -f %{sysconf_dir}/.pw.sed $i > $i.tmp; sed -e '/SubSys[[:space:]]*Directory/I d' $i.tmp > $i; rm -f $i.tmp; fi; done; fi; }

#------ Main file
Summary:	Bacula - The Network Backup Solution
Name:		bacula
Version:	5.0.2
Release:	%mkrel 5
Epoch:		1
Group:		Archiving/Backup
License:	GPL v2
URL:		http://www.bacula.org/
Source0:	http://prdownloads.sourceforge.net/bacula/bacula-%{version}.tar.gz
Source5:	http://prdownloads.sourceforge.net/bacula/bacula-gui-%{_guiver}.tar.gz
Source6:	bacula.pam-0.77.bz2
Source7:	bacula.pam.bz2
Patch1:		bacula-mandriva-platform.patch
Patch3:		bacula-updatedb.diff
Patch5:		bacula-gui-php_header.diff
Patch7:		bacula-web-mdv_conf.diff
Patch9:		bacula-listen.diff
Patch10:	bacula-2.4.3-cats.patch
# Patches 12 and 13 are required for backports only
Patch12:	bacula-5.0.2-libwrap_nsl.diff
Patch13:	bacula-5.0.2-sqlite-threadsafe.diff
Patch14:	bacula-5.0.1-config_dir.patch
Patch15:	bacula-some_scripts_should_be_configuration_files.diff
# Fix string literal errors - AdamW 2008/12
Patch17:	bacula-5.0.2-literal.patch
Patch18:	bacula-backupdir.diff
Patch19:	bacula-openssl_linkage.patch
Patch20:	bacula-5.0.1-static-sql.patch
Patch22:	bacula-5.0.1-gzip.patch
BuildRequires:	X11-devel
BuildRequires:	cdrecord
BuildRequires:	dvd+rw-tools
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	libacl-devel
BuildRequires:	mkisofs
BuildRequires:	mtx
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
BuildRequires: 	openssl-devel
BuildRequires: 	perl-base
BuildRequires: 	python-devel
%if %{TCPW}
BuildRequires:	tcp_wrappers-devel
Requires:	tcp_wrappers
%endif
%if %{mdkversion} >= 200800
BuildRequires:	imagemagick
%else
BuildRequires:	ImageMagick
%endif
BuildRequires:	libtool
Buildroot:	%{_tmppath}/bacula-%{version}-%{release}-buildroot

%description
%{blurb}
Bacula is a set of computer programs that permit you (or the system
administrator) to manage backup, recovery, and verification of computer
data across a network of computers of different kinds. In technical terms,
it is a network client/server based backup program. Bacula is relatively
easy to use and efficient, while offering many advanced storage management
features that make it easy to find and recover lost or damaged files.

#--- lib
%package	-n %mklibname bacula
Summary:	Bacula shared libraries
Group:		Archiving/Backup

%description	-n %mklibname bacula
%{blurb}
Bacula is a set of computer programs that permit you (or the system
administrator) to manage backup, recovery, and verification of computer
data across a network of computers of different kinds. In technical terms,
it is a network client/server based backup program. Bacula is relatively
easy to use and efficient, while offering many advanced storage management
features that make it easy to find and recover lost or damaged files.

#--- common
%package	common
Summary:	Common files for bacula package
Group:		Archiving/Backup
Requires(post): rpm-helper
Requires(postun): rpm-helper
Conflicts:	bacula-dir-common < %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-mysql < %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-pgsql < %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-sqlite3 < %{epoch}:%{version}-%{release}
# bacula-dir-sqlite has been removed but we keep the conflict for upgrades
Conflicts:	bacula-dir-sqlite < %{epoch}:%{version}-%{release}
Conflicts:	bacula-fd < %{epoch}:%{version}-%{release}
Conflicts:	bacula-sd < %{epoch}:%{version}-%{release}
Conflicts:	bacula-console < %{epoch}:%{version}-%{release}
Conflicts:	bacula-console-wx < %{epoch}:%{version}-%{release}
Conflicts:	bacula-tray-monitor < %{epoch}:%{version}-%{release}

%description	common
%{blurb}
Bacula is a set of computer programs that permit you (or the system
administrator) to manage backup, recovery, and verification of computer
data across a network of computers of different kinds. In technical terms,
it is a network client/server based backup program. Bacula is relatively
easy to use and efficient, while offering many advanced storage management
features that make it easy to find and recover lost or damaged files.

#------ Directory service
%package	dir-common
Summary:	Bacula Director and Catalog services
Group:		Archiving/Backup
Requires(pre,postun):	bacula-common
Requires(preun):	rpm-helper
Requires:	bacula-common = %{epoch}:%{version}-%{release}
%if %{TCPW}
Requires:	tcp_wrappers
%endif
%if %{mdkversion} >= 200810
Suggests:	mail-server
%endif

%description	dir-common
%{blurb}
Bacula Director is the program that supervises all the backup, restore, verify
and archive operations. The system administrator uses the Bacula Director to
schedule backups and to recover files.
Catalog services are comprised of the software programs responsible for
maintaining the file indexes and volume databases for all files backed up.
The Catalog services permit the System Administrator or user to quickly locate
and restore any desired file, since it maintains a record of all Volumes used,
all Jobs run, and all Files saved.

#--- mysql
%if %{MYSQL}
%package	dir-mysql
Summary:	Bacula Director and Catalog services
Group:		Archiving/Backup
Requires:	mysql-client
%if %{mdkversion} >= 200810
Suggests:	mysql
%endif
BuildRequires:	mysql-devel >= 3.23
Requires:	bacula-dir-common = %{epoch}:%{version}-%{release}
Requires(post):	bacula-dir-common = %{epoch}:%{version}-%{release}
Requires(post): rpm-helper
Provides:	bacula-dir = %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-pgsql bacula-dir-sqlite3

%description	dir-mysql
%{blurb}
Bacula Director is the program that supervises all the backup, restore, verify
and archive operations. The system administrator uses the Bacula Director to
schedule backups and to recover files.
Catalog services are comprised of the software programs responsible for
maintaining the file indexes and volume databases for all files backed up.
The Catalog services permit the System Administrator or user to quickly locate
and restore any desired file, since it maintains a record of all Volumes used,
all Jobs run, and all Files saved.
This build requires MySQL to be installed separately as the catalog database.
%endif

#--- pgsql
%if %{PGSQL}
%package	dir-pgsql
Summary:	Bacula Director and Catalog services
Group:		Archiving/Backup
Requires:	postgresql
%if %{mdkversion} >= 200810
Suggests:	postgresql-server
%endif
%if %{mdkversion} < 200810
BuildRequires:	postgresql-devel
%else
%if %{mdkversion} < 201000
BuildRequires:	postgresql8.3-devel
%else
BuildRequires:	postgresql8.4-devel
%endif
%endif
Requires:	bacula-dir-common = %{epoch}:%{version}-%{release}
Requires(post):	bacula-dir-common = %{epoch}:%{version}-%{release}
Requires(post): rpm-helper
Provides:	bacula-dir = %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-mysql bacula-dir-sqlite3

%description	dir-pgsql
%{blurb}
Bacula Director is the program that supervises all the backup, restore, verify
and archive operations. The system administrator uses the Bacula Director to
schedule backups and to recover files.
Catalog services are comprised of the software programs responsible for
maintaining the file indexes and volume databases for all files backed up.
The Catalog services permit the System Administrator or user to quickly locate
and restore any desired file, since it maintains a record of all Volumes used,
all Jobs run, and all Files saved.
This build requires Postgres to be installed separately as the catalog database.
%endif

#--- sqlite3
%package	dir-sqlite3
Summary:	Bacula Director and Catalog services
Group:		Archiving/Backup
Requires:	sqlite3-tools >= 3.4.2
BuildRequires:	sqlite3-devel >= 3.4.2
Requires:	bacula-dir-common = %{epoch}:%{version}-%{release}
Requires(post):	bacula-dir-common = %{epoch}:%{version}-%{release}
Requires(post): rpm-helper
Provides:	bacula-dir = %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-mysql bacula-dir-pgsql
# bacula-dir-sqlite has been removed we now provide it for upgrades
Obsoletes:	bacula-dir-sqlite
Provides:	bacula-dir-sqlite = %{epoch}:%{version}-%{release}

%description	dir-sqlite3
%{blurb}
Bacula Director is the program that supervises all the backup, restore, verify
and archive operations. The system administrator uses the Bacula Director to
schedule backups and to recover files.
Catalog services are comprised of the software programs responsible for
maintaining the file indexes and volume databases for all files backed up.
The Catalog services permit the System Administrator or user to quickly locate
and restore any desired file, since it maintains a record of all Volumes used,
all Jobs run, and all Files saved.
This build uses an embedded sqlite catalog database.

#------ Console

#--- main console
%package	console
Summary:	Bacula Console
Group:		Archiving/Backup
Requires:	bacula-common = %{epoch}:%{version}-%{release}
BuildRequires:	readline-devel
BuildRequires:	termcap-devel
Requires:	usermode-consoleonly

%description	console
%{blurb}
Bacula Console is the program that allows the administrator or user to
communicate with the Bacula Director.
This is the text only console interface.

#--- console-wx
%if %{WXWINDOWS}
%package	console-wx
Summary:	Bacula wxWindows Console
Group:		Archiving/Backup
BuildRequires:	wxgtku-devel
Requires:	bacula-common = %{epoch}:%{version}-%{release}
Requires:	usermode, usermode-consoleonly

%description	console-wx
%{blurb}
Bacula Console is the program that allows the administrator or user to
communicate with the Bacula Director.
This is the wxWindows GUI interface.
%endif

#--- console-bat
%if %{BAT}
%package	bat
Summary:	Bacula Administration Tool
Group:		Archiving/Backup
BuildRequires:	qt4-devel >= 4.2
BuildRequires:	libqwt-devel >= 5.0.2
Requires:	bacula-common = %{epoch}:%{version}-%{release}
Requires:	usermode, usermode-consoleonly

%description	bat
%{blurb}
This is the Bacula Administration Tool package. It is an add-on to
the client or server packages.
%endif

#------ File services

%package	fd
Summary:	Bacula File services (Client)
Group:		Archiving/Backup
Requires:	bacula-common = %{epoch}:%{version}-%{release}
Requires(post): rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	bacula-common
%if %{TCPW}
Requires:	tcp_wrappers
%endif

%description	fd
%{blurb}
Bacula File services (or Client program) is the software program that is
installed on the machine to be backed up. It is specific to the operating
system on which it runs and is responsible for providing the file attributes
and data when requested by the Director. The File services are also responsible
for the file system dependent part of restoring the file attributes and data
during a recovery operation.
This program runs as a daemon on the machine to be backed up, and in some of
the documentation, the File daemon is referred to as the Client (for example in
Bacula configuration file).

#------ Storage services
%package	sd
Summary:	Bacula Storage services
Group:		Archiving/Backup
Requires:	bacula-common = %{epoch}:%{version}-%{release}
Requires(post): rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	bacula-common
%if %{TCPW}
Requires:	tcp_wrappers
%endif

%description	sd
%{blurb}
Bacula Storage services consist of the software programs that perform the
storage and recovery of the file attributes and data to the physical backup
media or volumes. In other words, the Storage daemon is responsible for reading
and writing your tapes (or other storage media, e.g. files).
The Storage services runs as a daemon on the machine that has the backup
device (usually a tape drive).

#------ WEB gui
%if %{GUI}
%package	gui-web
Summary:	Bacula Web GUI
Group:		Archiving/Backup
Requires:	bacula-common = %{epoch}:%{version}-%{release}
Requires:	webserver
Requires:	apache-mod_php
Requires:	php-pear
Requires:	php-pear-DB
Requires:	php-gd
Requires:	phplot
Requires:	php-smarty

%description	gui-web
%{blurb}
Bacula is a set of computer programs that permit you (or the system
administrator) to manage backup, recovery, and verification of computer
data across a network of computers of different kinds. In technical terms,
it is a network client/server based backup program. Bacula is relatively
easy to use and efficient, while offering many advanced storage management
features that make it easy to find and recover lost or damaged files.

Contains the web gui

You need to install MySQL and php-mysql or PostgreSQL and php-pgsql if you want
to use either of them as the backend database.

#------ GUI-bimagemgr
%package	gui-bimagemgr
Summary:	Bacula Image Manager
Group:		Archiving/Backup
Requires:	bacula-common = %{epoch}:%{version}-%{release}
Requires:	webserver
Requires: 	perl-DBI
Requires:	perl-DBD-mysql

%description	gui-bimagemgr
%{blurb}
Bacula is a set of computer programs that permit you (or the system
administrator) to manage backup, recovery, and verification of computer
data across a network of computers of different kinds. In technical terms,
it is a network client/server based backup program. Bacula is relatively
easy to use and efficient, while offering many advanced storage management
features that make it easy to find and recover lost or damaged files.

Contains the bacula image manager cgi-bin

#------ GUI-brestore
%package	gui-brestore
Summary:	Bacula Image Manager
Group:		Archiving/Backup
Requires:	bacula-common = %{epoch}:%{version}-%{release}
Requires:	usermode, usermode-consoleonly

%description	gui-brestore
%{blurb}
Bacula is a set of computer programs that permit you (or the system
administrator) to manage backup, recovery, and verification of computer
data across a network of computers of different kinds. In technical terms,
it is a network client/server based backup program. Bacula is relatively
easy to use and efficient, while offering many advanced storage management
features that make it easy to find and recover lost or damaged files.

brestore is a file restore interface
%endif

#------ Tray monitor
%if %{TRAY}
%package	tray-monitor
Summary:	Bacula Tray Monitor
Group:		Archiving/Backup
BuildRequires:	gtk2-devel >= 2.4
Requires:	bacula-common = %{epoch}:%{version}-%{release}
Requires:	usermode, usermode-consoleonly

%description	tray-monitor
%{blurb}
The tray monitor for bacula.
%endif

#%package -n	nagios-check_bacula
#Summary:	The check_bacula plugin for nagios
#Group:		Networking/Other
#
#%description -n	nagios-check_bacula
#The check_bacula plugin for nagios.

%prep

%setup -q
%setup -q -D -T -a 5
mv bacula-gui-%{_guiver} gui
%patch1 -p1 -b .mandriva
%patch3 -p1 -b .updatedb
%patch5 -p0 -b .php_header
%patch7 -p1 -b .webconf
%patch9 -p1 -b .listen
%patch10 -p1 -b .cats
%patch12 -p1 -b .wrap
%patch13 -p1 -b .sqlite_thread
%patch14 -p1 -b .config
%patch15 -p1 -b .some_scripts_should_be_configuration_files
%patch17 -p1 -b .literal
%patch18 -p1 -b .backupdir
%patch19 -p1 -b .openssl_linkage
%patch20 -p1 -b .static
%patch22 -p1 -b .gzip

# fix conditional pam config file
%if %{mdkversion} < 200610
bzcat %{SOURCE6} > bacula.pam
%else
bzcat %{SOURCE7} > bacula.pam
%endif

%if %{TCPW}
%define _configure_tcpw --with-tcp-wrappers
%else
%define _configure_tcpw %{nil}
%endif
%define _configure_common --enable-smartalloc --localstatedir=/var/lib --sysconfdir=%{sysconf_dir} --with-working-dir=%{working_dir} --with-scriptdir=%{script_dir} --with-plugindir=%{script_dir} --with-subsys-dir=%{subsysdir} --with-python --with-openssl --disable-conio --with-db-name=bacula --with-db-user=bacula %{_configure_tcpw} --with-archivedir=%{archivedir} --with-hostname=localhost --with-basename=localhost --with-smtp-host=localhost --with-dir-user=bacula --with-dir-group=bacula --with-sd-user=bacula --with-sd-group=tape --with-fd-user=bacula --with-fd-group=bacula

#--disable-shared --enable-static 
# workaround fix-libtool-ltmain-from-overlinking bug
mv autoconf/ltmain.sh .
ln -s ../ltmain.sh autoconf

# workaround for --with-hostname not workibng
find src -name \*.conf.in -exec sed -i -e 's/@hostname@/@basename@/' {} \;

%build
export QMAKE="/usr/lib/qt4/bin/qmake"

%serverbuild

# disable FORTIFY_SOURCE http://www.mail-archive.com/bacula-devel@lists.sourceforge.net/msg01786.html
export CFLAGS="$(echo $CFLAGS|sed s/-D_FORTIFY_SOURCE=.//)"

%if %{MYSQL}
%configure --with-mysql \
	%_configure_common \
	--without-postgresql --without-sqlite3 \
	--disable-bwx-console --disable-bat --disable-tray-monitor
%make

# we have to do this because of the shared libraries
for z in src/dird/bacula-dir src/stored/bscan src/tools/dbcheck; do
	libtool --silent --mode=install install $z `pwd`/$z-mysql
done

for i in src/cats/*_mysql_*.in; do
    mv ${i%.in} $i
done
%make clean
%endif

%if %{PGSQL}
%configure --with-postgresql \
	%_configure_common \
	--without-mysql --without-sqlite3 \
	--disable-bwx-console --disable-bat --disable-tray-monitor
%make

# we have to do this because of the shared libraries
for z in src/dird/bacula-dir src/stored/bscan src/tools/dbcheck; do
	libtool --silent --mode=install install $z `pwd`/$z-postgresql
done

for i in src/cats/*_postgresql*.in; do
    mv ${i%.in} $i
done
%make clean
%endif

# now build sqlite3 and the rest of GUI tools

%configure --with-sqlite3 \
	%_configure_common \
	--without-mysql --without-postgresql \
%if %{WXWINDOWS}
	--enable-bwx-console \
%endif
%if %{TRAY}
	--enable-tray-monitor \
%endif
%if %{BAT}
	--enable-bat \
	--with-qwt=%{_prefix} \
%endif
        --with-dir-password="XXX_REPLACE_WITH_DIRECTOR_PASSWORD_XXX" \
        --with-fd-password="XXX_REPLACE_WITH_CLIENT_PASSWORD_XXX" \
        --with-sd-password="XXX_REPLACE_WITH_STORAGE_PASSWORD_XXX" \
        --with-mon-dir-password="XXX_REPLACE_WITH_DIRECTOR_MONITOR_PASSWORD_XXX" \
        --with-mon-fd-password="XXX_REPLACE_WITH_CLIENT_MONITOR_PASSWORD_XXX" \
        --with-mon-sd-password="XXX_REPLACE_WITH_STORAGE_MONITOR_PASSWORD_XXX" \

%make

# we have to do this because of the shared libraries
for z in src/dird/bacula-dir src/stored/bscan src/tools/dbcheck; do
	libtool --silent --mode=install install $z `pwd`/$z-sqlite3
done

%if %{GUI}
# Now we build the gui
(
  cd gui
  %configure --with-bacula="${PWD%/*}" \
	%_configure_common
  %make
)
%endif

%install
rm -rf %{buildroot}

# do not use %%makeinstall here
%make install DESTDIR=%{buildroot} dir_user= dir_group=

#lazy me
mv %{buildroot}%{script_dir}/make_catalog_backup.pl %{buildroot}%{sysconf_dir}/scripts/make_catalog_backup.pl

# install the catalog scripts and binaries
for db_type in \
%if %{MYSQL}
	mysql \
%endif
%if %{PGSQL}
	postgresql \
%endif
	sqlite3; do
    install -m 755 updatedb/update_${db_type}_tables_*_to_? %{buildroot}%{script_dir}
    install -m 755 updatedb/update_${db_type}_tables_*_to_?? %{buildroot}%{script_dir}
    for f in create_${db_type}_database drop_${db_type}_database drop_${db_type}_tables \
	grant_${db_type}_privileges make_${db_type}_tables update_${db_type}_tables ; do
    	install -m 755 src/cats/$f %{buildroot}%{script_dir}
	ln -snf $f %{buildroot}%{script_dir}/${f/${db_type}/bacula}
    done
    install -m 755 src/dird/bacula-dir-${db_type} %{buildroot}%{_sbindir}
    install -m 755 src/stored/bscan-${db_type} %{buildroot}%{_sbindir}
    install -m 755 src/tools/dbcheck-${db_type} %{buildroot}%{_sbindir}
done

# required to upgrade sqlite 2 database to sqlite 3
install -m 755 updatedb/update_sqlite_tables_?_to_[4-8] %{buildroot}%{script_dir}

# install the init scripts
install -d %{buildroot}%{_initrddir} %{buildroot}%{_sysconfdir}/sysconfig
install -m 755 platforms/mandriva/bacula-dir %{buildroot}%{_initrddir}/bacula-dir
install -m 755 platforms/mandriva/bacula-fd %{buildroot}%{_initrddir}/bacula-fd
install -m 755 platforms/mandriva/bacula-sd %{buildroot}%{_initrddir}/bacula-sd
install -m 644 platforms/mandriva/sysconfig %{buildroot}%{_sysconfdir}/sysconfig/bacula

# install the logrotate file
install -d %{buildroot}%{_sysconfdir}/logrotate.d
cp scripts/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/bacula-dir

install -d %{buildroot}%{working_dir}
install -D -d %{buildroot}%{archivedir}/bacula-restores

install -d %{buildroot}%{_sysconfdir}/security/console.apps
install -d %{buildroot}%{_sysconfdir}/pam.d
install -d %{buildroot}%{_bindir}

cat << EOF > %{buildroot}%{_sysconfdir}/security/console.apps/bconsole
USER=root
PROGRAM=%{_sbindir}/bconsole
SESSION=true
EOF

install -m0644 bacula.pam %{buildroot}%{_sysconfdir}/pam.d/bconsole
ln -s /usr/bin/consolehelper %{buildroot}%{_bindir}/bconsole

# install the menu stuff
%if %{WXWINDOWS} || %{BAT} || %{GUI}

%if %mdkversion <= 200700
install -d %{buildroot}%{_menudir}
%endif

install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}
%endif

%if %{WXWINDOWS} || %{BAT}
convert scripts/bacula.png -resize 16x16 %{buildroot}%{_miconsdir}/bacula.png
convert scripts/bacula.png -resize 32x32 %{buildroot}%{_iconsdir}/bacula.png
convert scripts/bacula.png -resize 48x48 %{buildroot}%{_liconsdir}/bacula.png
%endif

%if %{WXWINDOWS}

%if %mdkversion <= 200700
cat << EOF > %{buildroot}%{_menudir}/bacula-console-wx
?package(bacula-console-wx): \
command="%{_bindir}/bwx-console" \
icon="bacula.png" \
needs="x11" \
title="Bacula Console (wxWindows)" \
longtitle="Bacula Director Console" \
section="System/Archiving/Backup"
EOF
%endif

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-bacula-console-wx.desktop << EOF
[Desktop Entry]
Name=Bacula Console (wxWindows)
Comment=Bacula Director Console
Exec=%{_bindir}/bwx-console
Icon=bacula
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Archiving-Backup;Archiving;Utility;System;
EOF

cat << EOF > %{buildroot}%{_sysconfdir}/security/console.apps/bwx-console
USER=root
PROGRAM=%{_sbindir}/bwx-console
SESSION=true
EOF
install -m0644 bacula.pam %{buildroot}%{_sysconfdir}/pam.d/bwx-console
ln -s /usr/bin/consolehelper %{buildroot}%{_bindir}/bwx-console
cp -p src/console/bconsole.conf %{buildroot}%{sysconf_dir}/bwx-console.conf
%endif

%if %{BAT}
install -m0644 src/qt-console/bat.conf %{buildroot}%{sysconf_dir}/bat.conf

# make some icons
convert src/qt-console/images/bat_icon.png -resize 16x16 %{buildroot}%{_miconsdir}/bacula-bat.png
convert src/qt-console/images/bat_icon.png -resize 32x32 %{buildroot}%{_iconsdir}/bacula-bat.png
convert src/qt-console/images/bat_icon.png -resize 48x48 %{buildroot}%{_liconsdir}/bacula-bat.png

%if %mdkversion <= 200700
cat << EOF > %{buildroot}%{_menudir}/bacula-bat
?package(bacula-bat): \
command="%{_bindir}/bat" \
icon="bacula-bat.png" \
needs="x11" \
title="Bacula Administration Tool" \
longtitle="Bacula Administration Too" \
section="System/Archiving/Backup"
EOF
%endif

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-bacula-bat.desktop << EOF
[Desktop Entry]
Name=Bacula Administration Tool (QT4)
Comment=Bacula Administration Tool
Exec=%{_bindir}/bat
Icon=bacula-bat
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Archiving-Backup;Archiving;Utility;System;
EOF

cat << EOF > %{buildroot}%{_sysconfdir}/security/console.apps/bat
USER=root
PROGRAM=%{_sbindir}/bat
SESSION=true
EOF
install -m0644 bacula.pam %{buildroot}%{_sysconfdir}/pam.d/bat
ln -s /usr/bin/consolehelper %{buildroot}%{_bindir}/bat
%endif

%if %{TRAY}

%if %mdkversion <= 200700
cat << EOF > %{buildroot}%{_menudir}/bacula-tray-monitor
?package(bacula-tray-monitor): \
command="%{_bindir}/bacula-tray-monitor" \
icon="bacula.png" \
needs="x11" \
title="Bacula Tray Monitor" \
longtitle="Bacula Tray Monitor" \
section="System/Archiving/Backup"
EOF
%endif

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-bacula-tray-monitor.desktop << EOF
[Desktop Entry]
Name=Bacula Tray Monitor
Comment=Bacula Tray Monitor
Exec=%{_bindir}/bacula-tray-monitor
Icon=bacula
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Archiving-Backup;Archiving;Utility;System;
EOF

cat << EOF > %{buildroot}%{_sysconfdir}/security/console.apps/bacula-tray-monitor
USER=root
PROGRAM=%{_sbindir}/bacula-tray-monitor
SESSION=true
EOF
install -m0644 bacula.pam %{buildroot}%{_sysconfdir}/pam.d/bacula-tray-monitor
ln -s /usr/bin/consolehelper %{buildroot}%{_bindir}/bacula-tray-monitor
%endif

# Touch temporary password replacement file
touch %{buildroot}%{sysconf_dir}/.pw.sed

# Remove unneeded script
%__rm -f %{buildroot}/%{script_dir}/{start,stop}mysql
%__rm -f %{buildroot}/%{_sbindir}/bacula
%__rm -f %{buildroot}/%{script_dir}/bacula
%__rm -f %{buildroot}/%{script_dir}/bacula_config
%__rm -f %{buildroot}/%{script_dir}/bacula-ctl-*
%__rm -f %{buildroot}/%{script_dir}/bconsole

# Remove development libraries
%__rm -f %{buildroot}/%{_libdir}/*.a
for i in %{buildroot}/%{_libdir}/*.la; do
	%__rm -f $i ${i%.la}.so
done

%if %{GUI}
# install of bimagemgr
install -d -m 0755 %{buildroot}/var/www/html/bimagemgr
install -d -m 0755 %{buildroot}/var/www/cgi-bin
install -d -m 0755 %{buildroot}/%{_sysconfdir}
cp gui/bimagemgr/bimagemgr.pl %{buildroot}/var/www/cgi-bin
cp gui/bimagemgr/config.pm %{buildroot}/var/www/cgi-bin/config.pm
cp gui/bimagemgr/create_cdimage_table.pl %{buildroot}/%{_sysconfdir}
cp gui/bimagemgr/*.{html,gif} %{buildroot}/var/www/html/bimagemgr

# install of bacula-web
install -d -m 0755 %{buildroot}/var/www/html/bacula
cp -rf gui/bacula-web %{buildroot}/var/www/html/bacula
rm -rf %{buildroot}/var/www/html/bacula/external_packages/{smarty,phplot}

install -d -m 0755 %{buildroot}/var/cache/httpd/bacula-web
install -d -m 0755 %{buildroot}%{sysconf_dir}/bacula-web
mv %{buildroot}/var/www/html/bacula/bacula-web/configs/bacula.conf %{buildroot}%{sysconf_dir}/bacula-web/bacula.conf
rm -rf %{buildroot}/var/www/html/bacula/bacula-web/{configs,templates_c}

# install of brestore
convert gui/brestore/brestore.png -resize 16x16 %{buildroot}%{_miconsdir}/brestore.png
convert gui/brestore/brestore.png -resize 32x32 %{buildroot}%{_iconsdir}/brestore.png
convert gui/brestore/brestore.png -resize 48x48 %{buildroot}%{_liconsdir}/brestore.png

%if %mdkversion <= 200700
cat << EOF > %{buildroot}%{_menudir}/bacula-gui-brestore
?package(bacula-gui-brestore): \
command="%{_bindir}/brestore" \
icon="brestore.png" \
needs="x11" \
title="Bacula Restoration GUI" \
longtitle="Bacula Restoration GUI" \
section="System/Archiving/Backup"
EOF
%endif

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-bacula-gui-brestore.desktop << EOF
[Desktop Entry]
Name=Bacula Restoration GUI
Comment=Bacula Restoration GUI
Exec=%{_bindir}/brestore
Icon=brestore
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Archiving-Backup;Archiving;Utility;System;
EOF

cat << EOF > %{buildroot}%{_sysconfdir}/security/console.apps/brestore
USER=root
PROGRAM=%{_sbindir}/brestore.pl
SESSION=true
EOF

install -m 0755 gui/brestore/brestore.pl %{buildroot}%{_sbindir}
install -d -m 0755 %{buildroot}%{_datadir}/brestore
cp gui/brestore/brestore.glade %{buildroot}%{_datadir}/brestore
cp bacula.pam %{buildroot}/etc/pam.d/brestore
ln -s /usr/bin/consolehelper %{buildroot}/usr/bin/brestore
%endif

# Nagios plugin does not works correctly with 3.0.0 yet :(
## install the nagios plugin
#install -d %{buildroot}%{_sysconfdir}/nagios/plugins.d
#install -d %{buildroot}%{_libdir}/nagios/plugins
#
#install -m0755 src/check_bacula/check_bacula %{buildroot}%{_libdir}/nagios/plugins/
#
#cat > %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_bacula.cfg << EOF
## 'check_bacula' command definition
#define command{
#	command_name	check_bacula
#	command_line	%{_libdir}/nagios/plugins/check_bacula -H \$HOSTADDRESS$ -D \$ARG1\$ -M \$ARG2\$ -K \$ARG3\$ -P \$ARG4\$
#	}
#EOF

%pre common
%_pre_useradd bacula %{working_dir} /bin/false

%postun common
%_postun_userdel bacula

%pre dir-common
# pre-2010.0 .pw.sed file used a different syntax which was changed with MES5-based .spec
# this will ensure correct upgrade for old distro versions
if [ -e %{sysconf_dir}/.pw.sed ]; then
        sed -i -e "s/#YOU MUST SET THE DIR PASSWORD#/XXX_REPLACE_WITH_DIRECTOR_PASSWORD_XXX/g" \
            -e "s/#YOU MUST SET THE FD PASSWORD#/XXX_REPLACE_WITH_CLIENT_PASSWORD_XXX/g" \
            -e "s/#YOU MUST SET THE SD PASSWORD#/XXX_REPLACE_WITH_STORAGE_PASSWORD_XXX/g" \
            -e "s/#YOU MUST SET THE MONITOR DIR PASSWORD#/XXX_REPLACE_WITH_DIRECTOR_MONITOR_PASSWORD_XXX/g" \
            -e "s/#YOU MUST SET THE MONITOR FD PASSWORD#/XXX_REPLACE_WITH_CLIENT_MONITOR_PASSWORD_XXX/g" \
            -e "s/#YOU MUST SET THE MONITOR SD PASSWORD#/XXX_REPLACE_WITH_STORAGE_MONITOR_PASSWORD_XXX/g" \
            %{sysconf_dir}/.pw.sed
fi
# generating passwords, ensuring it is not visible in process list
for string in XXX_REPLACE_WITH_DIRECTOR_PASSWORD_XXX XXX_REPLACE_WITH_CLIENT_PASSWORD_XXX XXX_REPLACE_WITH_STORAGE_PASSWORD_XXX XXX_REPLACE_WITH_DIRECTOR_MONITOR_PASSWORD_XXX XXX_REPLACE_WITH_CLIENT_MONITOR_PASSWORD_XXX XXX_REPLACE_WITH_STORAGE_MONITOR_PASSWORD_XXX; do
    if ! grep -qs "$string" %{sysconf_dir}/.pw.sed; then
	echo -n "s!$string!" >> %{sysconf_dir}/.pw.sed
	openssl rand -base64 33 | sed -e 's/$/!g/'  >> %{sysconf_dir}/.pw.sed
    fi
done

%post dir-common
%post_fix_config *

#we have to restart fd and sd if we changed their configuration file
if [ -x %{_initrddir}/bacula-fd ]; then
%{_initrddir}/bacula-fd condrestart
fi
if [ -x %{_initrddir}/bacula-sd ]; then
%{_initrddir}/bacula-sd condrestart
fi

%preun dir-common
%_preun_service bacula-dir

%if %{MYSQL}
%post dir-mysql
umask 077
for f in create_mysql_database drop_mysql_database drop_mysql_tables \
    grant_mysql_privileges make_mysql_tables update_mysql_tables ; do
    ln -snf $f %{script_dir}/${f/mysql/bacula}
done
ln -snf bacula-dir-mysql %{_sbindir}/bacula-dir
ln -snf bscan-mysql %{_sbindir}/bscan
ln -snf dbcheck-mysql %{_sbindir}/dbcheck
# NOTE: IF THIS FAILS DUE TO MYSQL NEEDING A PASSWORD YOU ARE ON YOUR OWN
# see /etc/bacula/scripts/make_catalog_backup.pl for an example of how it should be done
DB_VER=`mysql bacula -e 'select * from Version;' 2>/dev/null | tail -n 1`
if [ -z "$DB_VER" ]; then
    echo "Hmm, doesn't look like you have an existing database."
    if [ -e %{working_dir}/rpm_db.log ]; then
	mv %{working_dir}/rpm_db.log %{working_dir}/rpm_db.log.old
    fi
    echo "Creating MySQL bacula database..."
    %{script_dir}/create_mysql_database >> %{working_dir}/rpm_db.log 2>&1
    echo "Creating bacula tables..."
    %{script_dir}/make_mysql_tables >> %{working_dir}/rpm_db.log 2>&1
    echo "Granting privileges for MySQL user bacula..."
    %{script_dir}/grant_mysql_privileges >> %{working_dir}/rpm_db.log 2>&1
    mysql bacula -e 'select * from Version;' > /dev/null 2>&1
    if [ $? != 0 ]; then
	echo "automatic database creation failed!" 1>&2
	echo "see log file %{working_dir}/rpm_db.log" 1>&2
	echo "if this is the first bacula installation" 1>&2
	echo "please check and run the following scripts:" 1>&2
	echo "	%{script_dir}/create_bacula_database" 1>&2
	echo "	%{script_dir}/make_bacula_tables" 1>&2
	echo "	%{script_dir}/grant_bacula_privileges" 1>&2
	echo "else manually update the database to version %{_cur_db_ver} using the scripts:" 1>&2
	echo "	%{script_dir}/update_mysql_tables_X_to_Y" 1>&2
	echo "and:" 1>&2
	echo "	%{script_dir}/update_bacula_tables" 1>&2
    fi
elif [ "$DB_VER" -lt "4" ]; then
    echo "ERROR: your bacula database version is too old to be upgraded automatically" 1>&2
    echo "save and drop any existing database" 1>&2
    echo "and recreate it using the following scripts:" 1>&2
    echo "	%{script_dir}/grant_bacula_privileges" 1>&2
    echo "	%{script_dir}/create_bacula_database" 1>&2
    echo "	%{script_dir}/make_bacula_tables" 1>&2
elif [ "$DB_VER" -lt "%{_cur_db_ver}" ]; then
    echo "Backing up bacula tables"
    mysqldump -f --opt bacula | bzip2 > %{working_dir}/bacula_backup.sql.bz2
    if [ -e %{working_dir}/rpm_db.log ]; then
	mv %{working_dir}/rpm_db.log %{working_dir}/rpm_db.log.old
    fi
    echo "Upgrading bacula tables"
    for v in `seq $DB_VER $(( %{_cur_db_ver} - 2 ))`; do
	%{script_dir}/update_mysql_tables_${v}_to_$(($v + 1)) >> %{working_dir}/rpm_db.log 2>&1
    done
    %{script_dir}/update_bacula_tables >> %{working_dir}/rpm_db.log 2>&1
    NDB_VER=`mysql bacula -e 'select * from Version;' 2>/dev/null | tail -n 1`
    if [ "$NDB_VER" -lt "%{_cur_db_ver}" ]; then
	echo "There was a problem updating Bacula MySQL database from version $DB_VER to %{_cur_db_ver}" 1>&2
	echo "see log file %{working_dir}/rpm_db.log" 1>&2
	echo "manually update the database to version %{_cur_db_ver} using the scripts:" 1>&2
	echo "	%{script_dir}/update_mysql_tables_X_to_Y" 1>&2
	echo "and:" 1>&2
	echo "	%{script_dir}/update_bacula_tables" 1>&2
    else
	echo "Bacula MySQL database updated to version $NDB_VER"
	echo "see log file %{working_dir}/rpm_db.log"
	echo "If bacula works correctly you can remove the backup file %{working_dir}/bacula_backup.sql.bz2"
    fi
fi
chown -R bacula:bacula %{working_dir}
chmod -R u+rX,go-rwx %{working_dir}
%_post_service bacula-dir
%endif

%if %{PGSQL}
%post dir-pgsql
umask 077
for f in create_postgresql_database drop_postgresql_database drop_postgresql_tables \
    grant_postgresql_privileges make_postgresql_tables update_postgresql_tables ; do
    ln -snf $f %{script_dir}/${f/postgresql/bacula}
done
ln -snf bacula-dir-postgresql %{_sbindir}/bacula-dir
ln -snf bscan-postgresql %{_sbindir}/bscan
ln -snf dbcheck-postgresql %{_sbindir}/dbcheck
# NOTE: IF THIS FAILS DUE TO PSQL NEEDING A PASSWORD YOU ARE ON YOUR OWN
# see /etc/bacula/scripts/make_catalog_backup.pl for an example of how it should be done
DB_VER=`su - postgres -c "psql bacula -A -t -c 'select * from Version;'" 2>/dev/null`
if [ -z "$DB_VER" ]; then
    echo "Hmm, doesn't look like you have an existing database."
    if [ -e %{working_dir}/rpm_db.log ]; then
	mv %{working_dir}/rpm_db.log %{working_dir}/rpm_db.log.old
    fi
    echo "Creating PostgreSQL bacula database..."
    su - postgres -c %{script_dir}/create_postgresql_database >> %{working_dir}/rpm_db.log 2>&1
    echo "Creating bacula tables..."
    su - postgres -c %{script_dir}/make_postgresql_tables >> %{working_dir}/rpm_db.log 2>&1
    echo "Granting privileges for PostgreSQL user bacula..."
    su - postgres -c %{script_dir}/grant_postgresql_privileges >> %{working_dir}/rpm_db.log 2>&1
    su - postgres -c "psql bacula -A -t -c 'select * from Version;'" >/dev/null 2>&1
    if [ $? != 0 ]; then
	echo "automatic database creation failed!" 1>&2
	echo "see log file %{working_dir}/rpm_db.log" 1>&2
	echo "if this is the first bacula installation" 1>&2
	echo "please check and run the following scripts:" 1>&2
	echo "	%{script_dir}/create_bacula_database" 1>&2
	echo "	%{script_dir}/make_bacula_tables" 1>&2
	echo "	%{script_dir}/grant_bacula_privileges" 1>&2
	echo "else manually update the database to version %{_cur_db_ver} using the scripts:" 1>&2
	echo "	%{script_dir}/update_mysql_tables_X_to_Y" 1>&2
	echo "and:" 1>&2
	echo "	%{script_dir}/update_bacula_tables" 1>&2
    fi
elif [ "$DB_VER" -lt "7" ]; then
    echo "ERROR: your bacula database version is too old to be upgraded automatically" 1>&2
    echo "save and drop any existing database" 1>&2
    echo "and recreate it using the following scripts:" 1>&2
    echo "	%{script_dir}/grant_bacula_privileges" 1>&2
    echo "	%{script_dir}/create_bacula_database" 1>&2
    echo "	%{script_dir}/make_bacula_tables" 1>&2
elif [ "$DB_VER" -lt "%{_cur_db_ver}" ]; then
    echo "Backing up bacula tables"
    su - postgres -c "pg_dump bacula" | bzip2 > %{working_dir}/bacula_backup.sql.bz2
    if [ -e %{working_dir}/rpm_db.log ]; then
	mv %{working_dir}/rpm_db.log %{working_dir}/rpm_db.log.old
    fi
    echo "Upgrading bacula tables"
    for v in `seq $DB_VER $(( %{_cur_db_ver} - 2 ))`; do
	su - postgres -c "%{script_dir}/update_postgresql_tables_${v}_to_$(($v + 1))" >> %{working_dir}/rpm_db.log 2>&1
    done
    su - postgres -c "%{script_dir}/update_bacula_tables" >> %{working_dir}/rpm_db.log 2>&1
    NDB_VER=`su - postgres -c "psql bacula -A -t -c 'select * from Version;'" 2>/dev/null`
    if [ "$NDB_VER" -lt "%{_cur_db_ver}" ]; then
	echo "There was a problem updating Bacula PostgreSQL database from version $DB_VER to %{_cur_db_ver}" 1>&2
	echo "see log file %{working_dir}/rpm_db.log" 1>&2
	echo "manually update the database to version %{_cur_db_ver} using the scripts:" 1>&2
	echo "	%{script_dir}/update_postgresql_tables_X_to_Y" 1>&2
	echo "and:" 1>&2
	echo "	%{script_dir}/update_bacula_tables" 1>&2
    else
	echo "Bacula PostgreSQL database updated to version $NDB_VER"
	echo "see log file %{working_dir}/rpm_db.log"
	echo "If bacula works correctly you can remove the backup file %{working_dir}/bacula_backup.sql.bz2"
    fi
fi
chown -R bacula:bacula %{working_dir}
chmod -R u+rX,go-rwx %{working_dir}
%_post_service bacula-dir
%endif

%post dir-sqlite3
umask 077
for f in create_sqlite3_database drop_sqlite3_database drop_sqlite3_tables \
    grant_sqlite3_privileges make_sqlite3_tables update_sqlite3_tables ; do
    ln -snf $f %{script_dir}/${f/sqlite3/bacula}
done
ln -snf bacula-dir-sqlite3 %{_sbindir}/bacula-dir
ln -snf bscan-sqlite3 %{_sbindir}/bscan
ln -snf dbcheck-sqlite3 %{_sbindir}/dbcheck
if [ -s %{working_dir}/bacula.db -a -x /usr/bin/sqlite ]; then
	DB2_VER=`echo "select * from Version;" | \
	    sqlite %{working_dir}/bacula.db 2>/dev/null | tail -n 1`
fi
if [ -n "$DB2_VER" ]; then
    # we have an sqlite2 db 
    echo "SQLITE 2 database detected: will try to upgrade it."
    echo "a backup of the untouched database will be found in %{working_dir}/bacula_backup.sql.bz2"
    #TODO: check if bacula is running 
    #service bacula-dir stop
    echo ".dump" | sqlite %{working_dir}/bacula.db | \
	bzip2 > %{working_dir}/bacula_backup.sql.bz2 
    if [ -e %{working_dir}/rpm_db.log ]; then
	mv %{working_dir}/rpm_db.log %{working_dir}/rpm_db.log.old
    fi
    # try to upgrade it to minimum requirement for sqlite3
    for v in `seq $DB2_VER 7`; do
	%{script_dir}/update_sqlite_tables_${v}_to_$(($v + 1)) >> %{working_dir}/rpm_db.log 2>&1
    done
    touch %{working_dir}/bacula.db.new
    echo .dump | sqlite %{working_dir}/bacula.db | \
	sed 's/ INTEGER UNSIGNED AUTOINCREMENT,/ INTEGER,/' | \
	sqlite3 %{working_dir}/bacula.db.new >> %{working_dir}/rpm_db.log 2>&1
    mv %{working_dir}/bacula.db.new %{working_dir}/bacula.db
fi
DB_VER=`echo "select * from Version;" | \
    sqlite3 %{working_dir}/bacula.db 2>/dev/null | tail -n 1`
if [ -z "$DB_VER" -a -n "$DB2_VER" ]; then
    echo "ERROR: conversion from Sqlite2 to Sqlite3 failed!" 1>&2
    echo "see log file %{working_dir}/rpm_db.log" 1>&2
    echo "save and drop any existing database" 1>&2
    echo "and recreate it using the following scripts:" 1>&2
    echo "	%{script_dir}/create_bacula_database" 1>&2
    echo "	%{script_dir}/make_bacula_tables" 1>&2
    echo "	%{script_dir}/grant_bacula_privileges" 1>&2
elif [ -z "$DB_VER" ]; then
# grant privileges and create tables
    if [ -e %{working_dir}/rpm_db.log ]; then
	mv %{working_dir}/rpm_db.log %{working_dir}/rpm_db.log.old
    fi
    if [ -s %{working_dir}/bacula.db ]; then
	echo "found a possibly corrupt %{working_dir}/bacula.db" 1>&2
	echo "renaming to: %{working_dir}/bacula.db.$$" 1>&2
	mv %{working_dir}/bacula.db %{working_dir}/bacula.db.$$
    fi
    %{script_dir}/create_bacula_database >> %{working_dir}/rpm_db.log 2>&1
    %{script_dir}/make_bacula_tables >> %{working_dir}/rpm_db.log 2>&1
    %{script_dir}/grant_bacula_privileges >> %{working_dir}/rpm_db.log 2>&1
    if [ $? != 0 ]; then
	echo "automatic database creation failed!" 1>&2
	echo "see log file %{working_dir}/rpm_db.log" 1>&2
	echo "if this is the first bacula installation" 1>&2
	echo "please check and run the following scripts:" 1>&2
	echo "	%{script_dir}/create_bacula_database" 1>&2
	echo "	%{script_dir}/make_bacula_tables" 1>&2
	echo "	%{script_dir}/grant_bacula_privileges" 1>&2
	echo "else manually update the database to version %{_cur_db_ver} using the scripts:" 1>&2
	echo "	%{script_dir}/update_sqlite3_tables_X_to_Y" 1>&2
	echo "and:" 1>&2
	echo "	%{script_dir}/update_bacula_tables" 1>&2
    fi
elif [ "$DB_VER" -lt "8" ]; then
    echo "ERROR: your bacula database version is too old to be upgraded automatically" 1>&2
    echo "save and drop any existing database" 1>&2
    echo "and recreate it using the following scripts:" 1>&2
    echo "	%{script_dir}/create_bacula_database" 1>&2
    echo "	%{script_dir}/make_bacula_tables" 1>&2
    echo "	%{script_dir}/grant_bacula_privileges" 1>&2
elif [ "$DB_VER" -lt "%{_cur_db_ver}" ]; then
    # in case we did a backup of an sqlite 2 database do not overwrite it
    if [ -z "$DB2_VER" ]; then
	echo "Backing up bacula tables"
	echo ".dump" | sqlite3 %{working_dir}/bacula.db | bzip2 > %{working_dir}/bacula_backup.sql.bz2
	if [ -e %{working_dir}/rpm_db.log ]; then
	    mv %{working_dir}/rpm_db.log %{working_dir}/rpm_db.log.old
	fi
    fi
    echo "Upgrading bacula tables"
    for v in `seq $DB_VER $((%{_cur_db_ver} - 2))`; do
	%{script_dir}/update_sqlite3_tables_${v}_to_$(($v + 1)) >> %{working_dir}/rpm_db.log 2>&1
    done
    %{script_dir}/update_bacula_tables >> %{working_dir}/rpm_db.log 2>&1

    NDB_VER=`echo "select * from Version;" | \
	sqlite3 %{working_dir}/bacula.db 2>/dev/null | tail -n 1`
    if [ "$NDB_VER" -lt "%{_cur_db_ver}" ]; then
	echo "There was a problem updating Bacula Sqlite3 database from version $DB_VER to %{_cur_db_ver}" 1>&2
	echo "see log file %{working_dir}/rpm_db.log" 1>&2
	echo "manually update the database to version %{_cur_db_ver} using the scripts:" 1>&2
	echo "	%{script_dir}/update_sqlite3_tables_X_to_Y" 1>&2
	echo "and:" 1>&2
	echo "	%{script_dir}/update_bacula_tables" 1>&2
    else
	echo "Bacula Sqlite3 database updated to version $NDB_VER"
	echo "see log file %{working_dir}/rpm_db.log"
	echo "If bacula works correctly you can remove the backup file %{working_dir}/bacula_backup.sql.bz2"
    fi
fi
chown -R bacula:bacula %{working_dir}
chmod -R u+rX,go-rwx %{working_dir}
%_post_service bacula-dir

%post fd
%post_fix_config bacula-fd
%_post_service bacula-fd

%preun fd
%_preun_service bacula-fd

%post sd
%post_fix_config bacula-sd
%_post_service bacula-sd

%preun sd
%_preun_service bacula-sd

%pre console
if [ -e %{sysconf_dir}/console.conf -a ! -e %{sysconf_dir}/bconsole.conf ]; then
    mv %{sysconf_dir}/console.conf %{sysconf_dir}/bconsole.conf
fi

%post console
%post_fix_config bconsole

%if %{WXWINDOWS}
%pre console-wx
if [ -e %{sysconf_dir}/wx-console.conf -a ! -e %{sysconf_dir}/bwx-console.conf ]; then
    mv %{sysconf_dir}/wx-console.conf %{sysconf_dir}/bwx-console.conf
fi

%post console-wx
%post_fix_config bwx-console
%if %mdkversion < 200900
%update_menus
%endif

%if %mdkversion < 200900
%postun console-wx
%clean_menus
%endif
%endif

%if %{BAT}
%post bat
%post_fix_config bat
%if %mdkversion < 200900
%update_menus
%endif

%if %mdkversion < 200900
%postun bat
%clean_menus
%endif
%endif

%if %{GUI}
%post gui-brestore
%if %mdkversion < 200900
%update_menus
%endif

%if %mdkversion < 200900
%postun gui-brestore
%clean_menus
%endif
%endif

%if %{TRAY}
%post tray-monitor
%post_fix_config tray-monitor
%if %mdkversion < 200900
%update_menus
%endif

%if %mdkversion < 200900
%postun tray-monitor
%clean_menus
%endif
%endif

#%post -n nagios-check_bacula
#%{_initrddir}/nagios condrestart > /dev/null 2>&1 || :
#
#%postun -n nagios-check_bacula
#if [ "$1" = "0" ]; then
#    %{_initrddir}/nagios condrestart > /dev/null 2>&1 || :
#fi

%clean
rm -rf %{buildroot}

%files -n %mklibname bacula
%defattr(0755,root,root,0755)
%{_libdir}/*.so

%files common
%defattr(0644,root,root,0755)
%{_docdir}/bacula
%if %{BAT}
%exclude %{_docdir}/bacula/html
%endif
%{_sysconfdir}/sysconfig/bacula
%dir %{sysconf_dir}
%dir %{script_dir}
%attr(0755,root,root) %{_sbindir}/btraceback
%attr(0755,root,root) %{_sbindir}/bsmtp
%attr(0755,root,root) %{_sbindir}/bregex
%attr(0755,root,root) %{_sbindir}/bwild
%{_libexecdir}/bacula/btraceback.gdb
%{_libexecdir}/bacula/btraceback.dbx
%attr(770, bacula, bacula) %dir %{working_dir}
%{_mandir}/man1/bsmtp.1*
%{_mandir}/man8/bacula.8*
%{_mandir}/man8/btraceback.8*
# exclude some manpage here if we are not building the related subpackage
%if ! %{TRAY}
%exclude %{_mandir}/man1/bacula-tray-monitor.1*
%endif
%if ! %{WXWINDOWS}
%exclude %{_mandir}/man1/bacula-bwxconsole.1*
%endif
%if ! %{BAT}
%exclude %{_mandir}/man1/bat.1*
%endif

%files dir-common
%defattr(0644,root,root,0755)
%attr(0640,root,bacula) %config(noreplace) %{sysconf_dir}/bacula-dir.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/bacula-dir
%{_mandir}/man8/bacula-dir.8*
%{_mandir}/man8/dbcheck.8*
%{_mandir}/man8/bscan.8*
%defattr (0755,root,root)
%attr(0755,root,root) %{_initrddir}/bacula-dir
%ghost %{_sbindir}/bacula-dir
%ghost %{_sbindir}/dbcheck
%ghost %{_sbindir}/bscan
%ghost %{script_dir}/create_bacula_database
%ghost %{script_dir}/drop_bacula_database
%ghost %{script_dir}/drop_bacula_tables
%ghost %{script_dir}/grant_bacula_privileges
%ghost %{script_dir}/make_bacula_tables
%ghost %{script_dir}/update_bacula_tables
%attr(0600,root,root) %ghost %{sysconf_dir}/.pw.sed
%dir %{sysconf_dir}/scripts
%attr(0754,root,bacula) %config(noreplace) %{sysconf_dir}/scripts/make_catalog_backup
%attr(0754,root,bacula) %config(noreplace) %{sysconf_dir}/scripts/make_catalog_backup.pl
%attr(0754,root,bacula) %config(noreplace) %{sysconf_dir}/scripts/delete_catalog_backup
%attr(0644,root,bacula) %config(noreplace) %{sysconf_dir}/scripts/query.sql

%if %{MYSQL}
%files dir-mysql
%{_sbindir}/bacula-dir-mysql
%{_sbindir}/dbcheck-mysql
%{_sbindir}/bscan-mysql
%{script_dir}/create_mysql_database
%{script_dir}/drop_mysql_database
%{script_dir}/drop_mysql_tables
%{script_dir}/grant_mysql_privileges
%{script_dir}/make_mysql_tables
%{script_dir}/update_mysql_tables*
%endif

%if %{PGSQL}
%files dir-pgsql
%{_sbindir}/bacula-dir-postgresql
%{_sbindir}/dbcheck-postgresql
%{_sbindir}/bscan-postgresql
%{script_dir}/create_postgresql_database
%{script_dir}/drop_postgresql_database
%{script_dir}/drop_postgresql_tables
%{script_dir}/grant_postgresql_privileges
%{script_dir}/make_postgresql_tables
%{script_dir}/update_postgresql_tables*
%endif

%files dir-sqlite3
%{_sbindir}/bacula-dir-sqlite3
%{_sbindir}/dbcheck-sqlite3
%{_sbindir}/bscan-sqlite3
%{script_dir}/create_sqlite3_database
%{script_dir}/drop_sqlite3_database
%{script_dir}/drop_sqlite3_tables
%{script_dir}/grant_sqlite3_privileges
%{script_dir}/make_sqlite3_tables
%{script_dir}/update_sqlite*_tables*

%files fd
%defattr(0755,root,root)
%attr(0640,root,bacula) %config(noreplace) %{sysconf_dir}/bacula-fd.conf
%attr(0755,root,root) %{_initrddir}/bacula-fd
%{_sbindir}/bacula-fd
%{script_dir}/bpipe-fd.so
%dir %attr(0770,bacula,bacula) %{archivedir}
%dir %attr(0770,bacula,bacula) %{archivedir}/bacula-restores

%attr(0644,root,root) %{_mandir}/man8/bacula-fd.8*

%files sd
%defattr(0755,root,root)
%attr(0755,root,root) %{_initrddir}/bacula-sd
%dir %{sysconf_dir}
%attr(0640,root,bacula) %config(noreplace) %{sysconf_dir}/bacula-sd.conf
%{_sbindir}/bacula-sd
%{_sbindir}/bcopy
%{_sbindir}/bextract
%{_sbindir}/bls
%{_sbindir}/btape
%dir %{sysconf_dir}/scripts
%attr(0754,root,bacula) %config(noreplace) %{sysconf_dir}/scripts/mtx-changer
%attr(0754,root,bacula) %config(noreplace) %{sysconf_dir}/scripts/mtx-changer.conf
%attr(0754,root,bacula) %config(noreplace) %{sysconf_dir}/scripts/disk-changer
%attr(0754,root,bacula) %config(noreplace) %{sysconf_dir}/scripts/dvd-handler
%defattr(0644,root,root,0755)
%{_mandir}/man8/bacula-sd.8*
%{_mandir}/man8/bcopy.8*
%{_mandir}/man8/bextract.8*
%{_mandir}/man8/bls.8*
%{_mandir}/man8/btape.8*
%dir %attr(0770,bacula,bacula) %{archivedir}

%files console
%defattr(0644,root,root,0755)
%attr(0640,root,bacula) %config(noreplace) %{sysconf_dir}/bconsole.conf
%config(noreplace) %{_sysconfdir}/security/console.apps/bconsole
%config(noreplace) %{_sysconfdir}/pam.d/bconsole
%attr(0755,root,root) %{_sbindir}/bconsole
%verify(link) %{_bindir}/bconsole
%{_mandir}/man8/bconsole.8*

%if %{WXWINDOWS}
%files console-wx
%defattr(0644,root,root,0755)
%attr(0640,root,bacula) %config(noreplace) %{sysconf_dir}/bwx-console.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/security/console.apps/bwx-console
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/bwx-console
%attr(0755,root,root) %{_sbindir}/bwx-console
%verify(link) %{_bindir}/bwx-console
%if %{mdkversion} <= 200700
%{_menudir}/bacula-console-wx
%endif
%{_iconsdir}/bacula.png
%{_miconsdir}/bacula.png
%{_liconsdir}/bacula.png
%{_datadir}/applications/mandriva-bacula-console-wx.desktop
%{_mandir}/man1/bacula-bwxconsole.1*
%endif

%if %{BAT}
%files bat
%defattr(0644,root,root,0755)
%{_docdir}/bacula/html
%attr(0640,root,bacula) %config(noreplace) %{sysconf_dir}/bat.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/security/console.apps/bat
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/bat
%attr(0755,root,root) %{_sbindir}/bat
%verify(link) %{_bindir}/bat
%if %{mdkversion} <= 200700
%{_menudir}/bacula-bat
%endif
%{_iconsdir}/bacula-bat.png
%{_miconsdir}/bacula-bat.png
%{_liconsdir}/bacula-bat.png
%{_datadir}/applications/mandriva-bacula-bat.desktop
%{_mandir}/man1/bat.1*
%endif

%if %{GUI}
%files gui-web
%dir %attr(0755,apache,apache) /var/www/html/bacula/
/var/www/html/bacula/*
%attr(0640,apache,apache) %config(noreplace) %{sysconf_dir}/bacula-web/bacula.conf
%dir %attr(0755,apache,apache) /var/cache/httpd/bacula-web

%files gui-bimagemgr
/var/www/html/bimagemgr/*.gif
/var/www/html/bimagemgr/*.html
/var/www/cgi-bin/bimagemgr.pl
/var/www/cgi-bin/config.pm
%{_sysconfdir}/create_cdimage_table.pl

%files gui-brestore
%defattr(0644,root,root,0755)
%doc COPYING README INSTALL ReleaseNotes
%attr(0644,root,root) %config(noreplace) /etc/security/console.apps/brestore
%attr(0644,root,root) %config(noreplace) /etc/pam.d/brestore
%attr(0755,root,root) %{_sbindir}/brestore.pl
%verify(link) %{_bindir}/brestore
%{_datadir}/brestore/brestore.glade
%if %{mdkversion} <= 200700
%{_menudir}/bacula-gui-brestore
%endif
%{_iconsdir}/brestore.png
%{_miconsdir}/brestore.png
%{_liconsdir}/brestore.png
%{_datadir}/applications/mandriva-bacula-gui-brestore.desktop
%endif

%if %{TRAY}
%files tray-monitor
%defattr(0644,root,root,0755)
%attr(0640,root,bacula) %config(noreplace) %{sysconf_dir}/tray-monitor.conf
%config(noreplace) %{_sysconfdir}/security/console.apps/bacula-tray-monitor
%config(noreplace) %{_sysconfdir}/pam.d/bacula-tray-monitor
%attr(0755,root,root) %{_sbindir}/bacula-tray-monitor
%verify(link) %{_bindir}/bacula-tray-monitor
%if %{mdkversion} <= 200700
%{_menudir}/bacula-tray-monitor
%endif
%{_iconsdir}/bacula.png
%{_miconsdir}/bacula.png
%{_liconsdir}/bacula.png
%{_datadir}/applications/mandriva-bacula-tray-monitor.desktop
%{_mandir}/man1/bacula-tray-monitor.1*
%endif
