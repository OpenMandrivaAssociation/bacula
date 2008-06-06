%define _guiver 2.4.0

%define _cur_db_ver 10

%define MYSQL 1
%define PGSQL 1
%define SQLITE3 1
%define GNOME 1
%define WXWINDOWS 1
%define BAT 1
%define TCPW 1
%define GUI 1
%define TRAY 1

%{?_with_mysql: %{expand: %%global MYSQL 1}}
%{?_without_mysql: %{expand: %%global MYSQL 0}}
%{?_with_pgsql: %{expand: %%global PGSQL 1}}
%{?_without_pgsql: %{expand: %%global PGSQL 0}}
%{?_with_sqlite3: %{expand: %%global SQLITE3 1}}
%{?_without_sqlite3: %{expand: %%global SQLITE3 0}}
%{?_with_gnome: %{expand: %%global GNOME 1}}
%{?_without_gnome: %{expand: %%global GNOME 0}}
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
%define post_fix_config() umask 0037; if [ -s %{_sysconfdir}/%{name}/.pw.sed ]; then for i in %{_sysconfdir}/%{name}/%{1}.conf %{_sysconfdir}/%{name}/%{1}.conf.rpmnew; do if [ -s $i ]; then sed -f %{_sysconfdir}/%{name}/.pw.sed $i > $i.tmp; sed -e '/SubSys[[:space:]]*Directory/I d' $i.tmp > $i; rm -f $i.tmp; fi; done; fi;

Summary:	Bacula - The Network Backup Solution
Name:		bacula
Version:	2.4.0
Release:	%mkrel 0.1
Epoch:		1
Group:		Archiving/Backup
License:	GPL
URL:		http://www.bacula.org/
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source5:	http://prdownloads.sourceforge.net/%{name}/%{name}-gui-%{_guiver}.tar.gz
Source6:	bacula.pam-0.77.bz2
Source7:	bacula.pam.bz2
Patch0:		bacula-config.diff
Patch1:		nagios-check_bacula.diff
Patch2:		bacula-pidfile.diff
Patch3:		bacula-updatedb.diff
Patch5:		bacula-gui-php_header.diff
Patch6:		bacula-manpages.diff
Patch7:		bacula-web-mdv_conf.diff
Patch8:		bacula-gnome2ssl.diff
Patch9:		bacula-listen.diff
Patch10:	bacula-cats.diff
Patch11:	bacula-db.diff
Patch12:	bacula-libwrap_nsl.diff
Patch13:	bacula-shared_backend_libs.diff
Patch14:	bacula-qt4_borkiness_fix.diff
Patch15:	bacula-some_scripts_should_be_configuration_files.diff
Patch16:	bacula-linkage_order.diff
BuildRequires:	X11-devel
BuildRequires:	cdrecord
BuildRequires:	dvd+rw-tools
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	latex2html
BuildRequires:	libacl-devel
BuildRequires:	mkisofs
BuildRequires:	mtx
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	termcap-devel
BuildRequires:	tetex-latex
BuildRequires:	zlib-devel
BuildRequires: 	openssl-devel
BuildRequires: 	perl-base
BuildRequires: 	python-devel
%if %{TCPW}
BuildRequires:	tcp_wrappers-devel
Requires:	tcp_wrappers
%endif
BuildRequires:	ImageMagick
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
%{blurb}
Bacula is a set of computer programs that permit you (or the system
administrator) to manage backup, recovery, and verification of computer
data across a network of computers of different kinds. In technical terms,
it is a network client/server based backup program. Bacula is relatively
easy to use and efficient, while offering many advanced storage management
features that make it easy to find and recover lost or damaged files.

%package	common
Summary:	Common files for bacula package
Group:		Archiving/Backup
Requires(post): rpm-helper
Requires(preun): rpm-helper
Conflicts:	bacula-dir-common < %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-mysql < %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-pgsql < %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-sqlite < %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-sqlite3 < %{epoch}:%{version}-%{release}
Conflicts:	bacula-fd < %{epoch}:%{version}-%{release}
Conflicts:	bacula-sd < %{epoch}:%{version}-%{release}
Conflicts:	bacula-console < %{epoch}:%{version}-%{release}
Conflicts:	bacula-console-gnome < %{epoch}:%{version}-%{release}
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

%package	dir-common
Summary:	Bacula Director and Catalog services
Group:		Archiving/Backup
Requires(post): rpm-helper perl-base sed bacula-common = %{epoch}:%{version}-%{release}
Requires(preun): rpm-helper perl-base sed bacula-common = %{epoch}:%{version}-%{release}
%if %{TCPW}
Requires:	tcp_wrappers
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

%if %{MYSQL}
%package	dir-mysql
Summary:	Bacula Director and Catalog services
Group:		Archiving/Backup
Requires:	mysql-client
BuildRequires:	mysql-devel >= 3.23
Requires:	bacula-dir-common
Provides:	bacula-dir = %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-pgsql bacula-dir-sqlite bacula-dir-sqlite3

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

%if %{PGSQL}
%package	dir-pgsql
Summary:	Bacula Director and Catalog services
Group:		Archiving/Backup
Requires:	postgresql
BuildRequires:	postgresql-devel
Requires:	bacula-dir-common
Provides:	bacula-dir = %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-mysql bacula-dir-sqlite bacula-dir-sqlite3

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

%if %{SQLITE3}
%package	dir-sqlite3
Summary:	Bacula Director and Catalog services
Group:		Archiving/Backup
Requires:	sqlite3-tools >= 3.4.2
BuildRequires:	sqlite3-devel >= 3.4.2
Requires:	bacula-dir-common
Provides:	bacula-dir = %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-mysql bacula-dir-pgsql bacula-dir-sqlite

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
%endif

%package	dir-sqlite
Summary:	Bacula Director and Catalog services
Group:		Archiving/Backup
Requires:	sqlite-tools
BuildRequires:	sqlite-devel
Requires:	bacula-dir-common
Provides:	bacula-dir = %{epoch}:%{version}-%{release}
Conflicts:	bacula-dir-mysql bacula-dir-pgsql bacula-dir-sqlite3
# this might allow urpmi to upgrade correctly
Obsoletes:	bacula-dir

%description	dir-sqlite
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

%package	console
Summary:	Bacula Console
Group:		Archiving/Backup
Requires(post): sed bacula-common = %{epoch}:%{version}-%{release}
Requires(preun): sed bacula-common = %{epoch}:%{version}-%{release}
BuildRequires:	termcap-devel
Requires:	usermode-consoleonly

%description	console
%{blurb}
Bacula Console is the program that allows the administrator or user to
communicate with the Bacula Director.
This is the text only console interface.

%if %{GNOME}
%package	console-gnome
Summary:	Bacula Gnome Console
Group:		Archiving/Backup
BuildRequires: libgnomeui2-devel
Requires(post): sed bacula-common = %{epoch}:%{version}-%{release}
Requires(preun): sed bacula-common = %{epoch}:%{version}-%{release}
Requires:	usermode, usermode-consoleonly

%description	console-gnome
%{blurb}
Bacula Console is the program that allows the administrator or user to
communicate with the Bacula Director.
This is the GNOME GUI interface.
%endif

%if %{WXWINDOWS}
%package	console-wx
Summary:	Bacula wxWindows Console
Group:		Archiving/Backup
%if %{mdkversion} >= 1020
BuildRequires:	wxGTK2.6-devel >= 2.6.1
%else
BuildRequires:	wxGTK2.4-devel
%endif
Requires(post): sed bacula-common = %{epoch}:%{version}-%{release}
Requires(preun): sed bacula-common = %{epoch}:%{version}-%{release}
Requires:	usermode, usermode-consoleonly

%description	console-wx
%{blurb}
Bacula Console is the program that allows the administrator or user to
communicate with the Bacula Director.
This is the wxWindows GUI interface.
%endif

%if %{BAT}
%package	bat
Summary:	Bacula Administration Tool
Group:		Archiving/Backup
BuildRequires:	qt4-devel >= 4.2
BuildRequires:	libqwt-devel >= 5.0.2
Requires(post): sed bacula-common = %{epoch}:%{version}-%{release}
Requires(preun): sed bacula-common = %{epoch}:%{version}-%{release}
Requires:	usermode, usermode-consoleonly

%description	bat
%{blurb}
This is the Bacula Administration Tool package. It is an add-on to 
the client or server packages.
%endif

%package	fd
Summary:	Bacula File services (Client)
Group:		Archiving/Backup
Requires(post): rpm-helper sed bacula-common = %{epoch}:%{version}-%{release}
Requires(preun):rpm-helper sed bacula-common = %{epoch}:%{version}-%{release}
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

%package	sd
Summary:	Bacula Storage services
Group:		Archiving/Backup
Requires(post): rpm-helper sed bacula-common = %{epoch}:%{version}-%{release}
Requires(preun):rpm-helper sed bacula-common = %{epoch}:%{version}-%{release}
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

%if %{GUI}
%package	gui-web
Summary:	Bacula Web GUI
Group:		Archiving/Backup
Requires(post): rpm-helper sed bacula-common = %{epoch}:%{version}-%{release}
Requires(preun):rpm-helper sed bacula-common = %{epoch}:%{version}-%{release}
Requires:	webserver
Requires:	php-pear
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

%package	gui-bimagemgr
Summary:	Bacula Image Manager
Group:		Archiving/Backup
Requires(post): rpm-helper sed bacula-common = %{epoch}:%{version}-%{release}
Requires(preun):rpm-helper sed bacula-common = %{epoch}:%{version}-%{release}
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
%endif

%if %{TRAY}
%package	tray-monitor
Summary:	Bacula Tray Monitor
Group:		Archiving/Backup
BuildRequires:	gtk2-devel >= 2.4
Requires(post): sed bacula-common = %{epoch}:%{version}-%{release}
Requires(preun): sed bacula-common = %{epoch}:%{version}-%{release}
Requires:	usermode, usermode-consoleonly

%description	tray-monitor
%{blurb}
The tray monitor for bacula.
%endif

%package -n	nagios-check_bacula
Summary:	The check_bacula plugin for nagios
Group:		Networking/Other

%description -n	nagios-check_bacula
The check_bacula plugin for nagios.

%prep

%setup -q
%setup -q -D -T -a 5
mv %{name}-gui-%{_guiver} gui
%patch0 -p1 -b .config
%patch1 -p0 -b .nagios-check_bacula
%patch2 -p0 -b .pidfile
%patch3 -p1 -b .updatedb
%patch5 -p0 -b .php_header
%patch6 -p0 -b .manpages
%patch7 -p1
%patch8 -p0 -b .gnome2ssl
%patch9 -p1 -b .listen
%patch10 -p0 -b .cats
%patch11 -p0 -b .db
%patch12 -p1 -b .wrap
%patch13 -p0 -b .shared_backend_libs
%patch14 -p0 -b .qt4_borkiness_fix
%patch15 -p1 -b .some_scripts_should_be_configuration_files
%patch16 -p0 -b .bacula-linkage_order

perl -spi -e 's/\@hostname\@/localhost/g' `find . -name \*.in`

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
%define _configure_common --enable-smartalloc --localstatedir=/var/lib --sysconfdir=%{_sysconfdir}/%{name} --with-working-dir=/var/lib/%{name} --with-scriptdir=%{_libexecdir}/%{name} --with-subsys-dir=/var/lock/subsys --with-python --with-openssl --with-readline --with-db-name=%{name} --with-db-user=%{name} %{_configure_tcpw}

# temprorary mdv hack because our qt/kde suite is fucked up, still!
perl -pi -e "s|qmake|/usr/lib/qt4/bin/qmake|g" autoconf/configure.in

pushd src
    tar -zxf ../examples/nagios/nagios_plugin_check_bacula.tgz
popd

%build
export QMAKE="/usr/lib/qt4/bin/qmake"

# reconstruct the autofoo stuff
pushd autoconf
    aclocal -I bacula-macros -I gettext-macros
popd
autoconf --prepend-include=./autoconf autoconf/configure.in > configure
chmod 755 configure

%serverbuild

%if %{MYSQL}
%configure --with-mysql \
	%_configure_common \
	--without-sqlite --without-postgresql --without-sqlite3 \
	--disable-gnome --disable-bwx-console --disable-bat --disable-tray-monitor
%make

# make the nagios plugin
pushd src/check_bacula
%make LIBS="-lpthread -ldl  -lintl -lssl -lcrypto"
popd

for i in src/dird/bacula-dir src/stored/bscan src/tools/dbcheck; do
    mv $i $i-mysql
done
for i in src/cats/*_mysql_*.in; do 
    mv ${i%.in} $i
done
%make clean
%endif

%if %{PGSQL}
%configure --with-postgresql \
	%_configure_common \
	--without-sqlite --without-mysql --without-sqlite3 \
	--disable-gnome --disable-bwx-console --disable-bat --disable-tray-monitor
%make
for i in src/dird/bacula-dir src/stored/bscan src/tools/dbcheck; do
    mv $i $i-postgresql
done
for i in src/cats/*_postgresql*.in; do 
    mv ${i%.in} $i
done
%make clean
%endif

%if %{SQLITE3}
%configure --with-sqlite3 \
	%_configure_common \
	--without-mysql --without-postgresql --without-sqlite \
	--disable-gnome --disable-bwx-console --disable-bat --disable-tray-monitor
%make
for i in src/dird/bacula-dir src/stored/bscan src/tools/dbcheck; do
    mv $i $i-sqlite3
done
for i in src/cats/*_sqlite3*.in; do 
    mv ${i%.in} $i
done
%make clean
%endif

%configure --with-sqlite \
	%_configure_common \
	--without-mysql --without-postgresql --without-sqlite3 \
%if %{GNOME}
	--enable-gnome \
%endif
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
	--with-dir-password="#FAKE#DIR#PASSWORD#" \
	--with-fd-password="#FAKE#FD#PASSWORD#" \
	--with-sd-password="#FAKE#SD#PASSWORD#" \
	--with-mon-dir-password="#FAKE#MON#DIR#PASSWORD#" \
  	--with-mon-fd-password="#FAKE#MON#FD#PASSWORD#" \
	--with-mon-sd-password="#FAKE#MON#SD#PASSWORD#" \

%make
for i in src/dird/bacula-dir src/stored/bscan src/tools/dbcheck; do
    mv $i $i-sqlite
    ln -s ${i##*/}-sqlite $i
done

%if %{GUI}
# Now we build the gui
( 
  cd gui
  %configure --with-bacula="${PWD%/*}"
  %make 
)
%endif

%install
rm -rf %{buildroot}

%makeinstall sysconfdir=%{buildroot}%{_sysconfdir}/%{name} scriptdir=%{buildroot}%{_libexecdir}/%{name} working_dir=%{buildroot}/var/lib/%{name}

# install the catalog scripts and binaries
for db_type in \
%if %{MYSQL}
	mysql \
%endif
%if %{PGSQL}
	postgresql \
%endif
%if %{SQLITE3}
	sqlite3 \
%endif
	sqlite; do
    install -m 755 updatedb/update_${db_type}_tables_?_to_? %{buildroot}%{_libexecdir}/%{name}
    for f in create_${db_type}_database drop_${db_type}_database drop_${db_type}_tables \
	grant_${db_type}_privileges make_${db_type}_tables update_${db_type}_tables ; do
    	install -m 755 src/cats/$f %{buildroot}%{_libexecdir}/%{name} 
	ln -snf $f %{buildroot}%{_libexecdir}/%{name}/${f/${db_type}/bacula}
    done
    install -m 755 src/dird/bacula-dir-${db_type} %{buildroot}%{_sbindir}
    install -m 755 src/stored/bscan-${db_type} %{buildroot}%{_sbindir}
    install -m 755 src/tools/dbcheck-${db_type} %{buildroot}%{_sbindir}
    ln -snf bacula-dir-${db_type} %{buildroot}%{_sbindir}/bacula-dir
    ln -snf bscan-${db_type} %{buildroot}%{_sbindir}/bscan
    ln -snf dbcheck-${db_type} %{buildroot}%{_sbindir}/dbcheck
done

# install the init scripts
install -d %{buildroot}%{_initrddir}
install -m 755 platforms/mandrake/bacula-dir %{buildroot}%{_initrddir}/bacula-dir
install -m 755 platforms/mandrake/bacula-fd %{buildroot}%{_initrddir}/bacula-fd
install -m 755 platforms/mandrake/bacula-sd %{buildroot}%{_initrddir}/bacula-sd

# install the logrotate file
install -d %{buildroot}%{_sysconfdir}/logrotate.d
cp scripts/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/bacula-dir

install -d %{buildroot}/var/lib/%{name}

install -d %{buildroot}%{_sysconfdir}/security/console.apps
install -d %{buildroot}%{_sysconfdir}/pam.d
install -d %{buildroot}%{_bindir}

cat << EOF > %{buildroot}%{_sysconfdir}/security/console.apps/bconsole
USER=root
PROGRAM=%{_sbindir}/bconsole
SESSION=true
EOF

install -m0644 bacula.pam %{buildroot}%{_sysconfdir}/pam.d/bconsole
ln -s consolehelper %{buildroot}%{_bindir}/bconsole

# install the menu stuff
%if %{GNOME} || %{WXWINDOWS} || %{BAT}

%if %mdkversion <= 200700
install -d %{buildroot}%{_menudir}
%endif

install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}

convert scripts/bacula.png -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert scripts/bacula.png -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert scripts/bacula.png -resize 48x48 %{buildroot}%{_liconsdir}/%{name}.png
%endif

%if %{GNOME}

%if %mdkversion <= 200700
cat << EOF > %{buildroot}%{_menudir}/%{name}-console-gnome
?package(%{name}-console-gnome): \
command="%{_bindir}/bgnome-console" \
icon="%{name}.png" \
needs="x11" \
title="Bacula Console (gnome)" \
longtitle="Bacula Director Console" \
section="System/Archiving/Backup"
EOF
%endif

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-console-gnome.desktop << EOF
[Desktop Entry]
Name=Bacula Console (gnome)
Comment=Bacula Director Console
Exec=%{_bindir}/bgnome-console
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Archiving-Backup;Archiving;Utility;System;
EOF

cat << EOF > %{buildroot}%{_sysconfdir}/security/console.apps/bgnome-console
USER=root
PROGRAM=%{_sbindir}/bgnome-console
SESSION=true
EOF
install -m0644 bacula.pam %{buildroot}%{_sysconfdir}/pam.d/bgnome-console
ln -s consolehelper %{buildroot}%{_bindir}/bgnome-console
%endif

%if %{WXWINDOWS}

%if %mdkversion <= 200700
cat << EOF > %{buildroot}%{_menudir}/%{name}-console-wx
?package(%{name}-console-wx): \
command="%{_bindir}/bwx-console" \
icon="%{name}.png" \
needs="x11" \
title="Bacula Console (wxWindows)" \
longtitle="Bacula Director Console" \
section="System/Archiving/Backup"
EOF
%endif

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-console-wx.desktop << EOF
[Desktop Entry]
Name=Bacula Console (wxWindows)
Comment=Bacula Director Console
Exec=%{_bindir}/bwx-console
Icon=%{name}
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
ln -s consolehelper %{buildroot}%{_bindir}/bwx-console
# we need to install the program files as well
#install -m 755 src/wx-console/wx-console %{buildroot}%{_sbindir}
#cp -p src/console/bconsole.conf %{buildroot}%{_sysconfdir}/%{name}/wx-console.conf
%endif

%if %{BAT}
install -m0755 src/qt-console/bat %{buildroot}%{_sbindir}/%{name}-bat
install -m0644 src/qt-console/bat.conf %{buildroot}%{_sysconfdir}/%{name}/bat.conf

# make some icons
convert src/qt-console/images/bat_icon.png -resize 16x16 %{buildroot}%{_miconsdir}/%{name}-bat.png
convert src/qt-console/images/bat_icon.png -resize 32x32 %{buildroot}%{_iconsdir}/%{name}-bat.png
convert src/qt-console/images/bat_icon.png -resize 48x48 %{buildroot}%{_liconsdir}/%{name}-bat.png

%if %mdkversion <= 200700
cat << EOF > %{buildroot}%{_menudir}/%{name}-bat
?package(%{name}-bat): \
command="%{_bindir}/%{name}-bat" \
icon="%{name}-bat.png" \
needs="x11" \
title="Bacula Administration Tool" \
longtitle="Bacula Administration Too" \
section="System/Archiving/Backup"
EOF
%endif

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-bat.desktop << EOF
[Desktop Entry]
Name=Bacula Administration Tool (QT4)
Comment=Bacula Administration Tool
Exec=%{_bindir}/%{name}-bat
Icon=%{name}-bat
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Archiving-Backup;Archiving;Utility;System;
EOF

cat << EOF > %{buildroot}%{_sysconfdir}/security/console.apps/%{name}-bat
USER=root
PROGRAM=%{_sbindir}/%{name}-bat
SESSION=true
EOF
install -m0644 bacula.pam %{buildroot}%{_sysconfdir}/pam.d/%{name}-bat
ln -s consolehelper %{buildroot}%{_bindir}/%{name}-bat

mv %{buildroot}%{_mandir}/man1/bat.1  %{buildroot}%{_mandir}/man1/%{name}-bat.1 
%endif

rm -f %{buildroot}%{_mandir}/man1/bat.1*

%if %{TRAY}

%if %mdkversion <= 200700
cat << EOF > %{buildroot}%{_menudir}/%{name}-tray-monitor
?package(%{name}-tray-monitor): \
command="%{_bindir}/bacula-tray-monitor" \
icon="%{name}.png" \
needs="x11" \
title="Bacula Tray Monitor" \
longtitle="Bacula Tray Monitor" \
section="System/Archiving/Backup"
EOF
%endif

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-tray-monitor.desktop << EOF
[Desktop Entry]
Name=Bacula Tray Monitor
Comment=Bacula Tray Monitor
Exec=%{_bindir}/bacula-tray-monitor
Icon=%{name}
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
ln -s consolehelper %{buildroot}%{_bindir}/bacula-tray-monitor
%endif

# Remove some left-over in the compil process to the correct path
%__rm -f %{buildroot}/%{_libdir}/%{name}/{start,stop}mysql 
%__rm -f %{buildroot}/%{_libdir}/%{name}/gconsole

perl -spi -e 's/"#FAKE#(\w+)#PASSWORD#"/#YOU MUST SET THE $1 PASSWORD#/' %{buildroot}%{_sysconfdir}/%{name}/*.conf
perl -spi -e 's/"#FAKE#MON#(\w+)#PASSWORD#"/#YOU MUST SET THE MONITOR $1 PASSWORD#/' %{buildroot}%{_sysconfdir}/%{name}/*.conf
touch %{buildroot}%{_sysconfdir}/%{name}/.pw.sed

%if %{GUI}
# install of bimagemgr
install -d -m 0755 %{buildroot}/var/www/html/bimagemgr
install -d -m 0755 %{buildroot}/var/www/cgi-bin
install -d -m 0755 %{buildroot}/%{_sysconfdir}
cp gui/bimagemgr/bimagemgr.pl %{buildroot}/var/www/cgi-bin
cp gui/bimagemgr/create_cdimage_table.pl %{buildroot}/%{_sysconfdir}
cp gui/bimagemgr/*.{html,gif} %{buildroot}/var/www/html/bimagemgr

# install of bacula-web
install -d -m 0755 %{buildroot}/var/www/html/bacula
cp -rf gui/bacula-web %{buildroot}/var/www/html/bacula
rm -rf %{buildroot}/var/www/html/bacula/external_packages/{smarty,phplot}

install -d -m 0755 %{buildroot}%{_sysconfdir}/bacula/bacula-web
install -d -m 0755 %{buildroot}/var/cache/httpd/bacula-web
mv %{buildroot}/var/www/html/bacula/bacula-web/configs/bacula.conf %{buildroot}%{_sysconfdir}/bacula/bacula-web/bacula.conf
rm -rf %{buildroot}/var/www/html/bacula/bacula-web/{configs,templates_c}
%endif

# install the nagios plugin
install -d %{buildroot}%{_sysconfdir}/nagios/plugins.d
install -d %{buildroot}%{_libdir}/nagios/plugins

install -m0755 src/check_bacula/check_bacula %{buildroot}%{_libdir}/nagios/plugins/

cat > %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_bacula.cfg << EOF
# 'check_bacula' command definition
define command{
	command_name	check_bacula
	command_line	%{_libdir}/nagios/plugins/check_bacula -H \$HOSTADDRESS$ -D \$ARG1\$ -M \$ARG2\$ -K \$ARG3\$ -P \$ARG4\$
	}
EOF

# duh?
install -m0755 scripts/btraceback %{buildroot}%{_sbindir}/
install -m0644 scripts/btraceback.gdb %{buildroot}%{_libdir}/bacula/
install -m0644 scripts/btraceback.dbx %{buildroot}%{_libdir}/bacula/
install -m0644 scripts/dvd-handler %{buildroot}%{_sysconfdir}/bacula/scripts/
install -m0644 scripts/mtx-changer %{buildroot}%{_sysconfdir}/bacula/scripts/
install -m0644 scripts/disk-changer %{buildroot}%{_sysconfdir}/bacula/scripts/

%pre common
%_pre_useradd bacula /var/lib/%{name} /bin/false

%postun common
%_postun_userdel bacula

%pre dir-common
/usr/bin/perl -e '
$confdir="%{_sysconfdir}/%{name}";
$conffile="$confdir/.pw.sed";
if ( -f "$conffile") {
	open(IN, "<$conffile") or die "$!";
	while (<IN>) {
		/#YOU MUST SET THE (.*) PASSWORD#/ && $already{$1}++;
	}
	close(IN);
}
mkdir("$confdir");
umask(0077);
open(IN, "/dev/random") or die "$!";
open(OUT, ">>$conffile") or die "$!";
foreach $c ("DIR","SD","FD","MONITOR DIR","MONITOR SD","MONITOR FD") {
next if ($already{$c});
read(IN, $buf, 32);
my $res = pack("u", $buf);
$res =~ s/^.//mg;
$res =~ s/\n//g;
$res =~ tr|` -_|AA-Za-z0-9+/|;
	print OUT "s!#YOU MUST SET THE $c PASSWORD#!\"$res\"!\n";
}
close (IN);
close (OUT);
'

%post dir-common
%post_fix_config *
%_post_service bacula-dir

%preun dir-common
%_preun_service bacula-dir

%if %{MYSQL}
%post dir-mysql
umask 077
for f in create_mysql_database drop_mysql_database drop_mysql_tables \
    grant_mysql_privileges make_mysql_tables update_mysql_tables ; do
    ln -snf $f %{_libexecdir}/%{name}/${f/mysql/bacula}
done
ln -snf bacula-dir-mysql %{_sbindir}/bacula-dir
ln -snf bscan-mysql %{_sbindir}/bscan
ln -snf dbcheck-mysql %{_sbindir}/dbcheck
# NOTE: IF THIS FAILS DUE TO MYSQL/PGSQL NEEDING A PASSWORD YOU ARE ON YOUR OWN
DB_VER=`mysql bacula -e 'select * from Version;' | tail -n 1 2>/dev/null`
if [ -z "$DB_VER" ]; then
	echo cannot connect to bacula catalog database
	echo if this is the first bacula installation please check
	echo and run the following scripts
	echo 	%{_libexecdir}/%{name}/grant_bacula_privileges
	echo 	%{_libexecdir}/%{name}/create_bacula_database
	echo 	%{_libexecdir}/%{name}/make_bacula_tables
	echo else manually update the database to version %{_cur_db_ver} using the script
	echo 	%{_libexecdir}/%{name}/update_bacula_tables
elif [ "$DB_VER" -lt "%{_cur_db_ver}" ]; then
	echo "Backing up bacula tables"
	mysqldump -f --opt bacula | bzip2 > /var/lib/%{name}/bacula_backup.sql.bz2
	echo "Upgrading bacula tables"
	if [ "$DB_VER" -lt "4" ]; then
		echo "your bacula database version is too old to be upgraded automatically"
	else
	    for v in `seq 5 $((%{_cur_db_ver} - 1))`; do
		if [ "$DB_VER" -lt "$v" ]; then
			%{_libexecdir}/%{name}/update_mysql_tables_$((v - 1))_to_$v
		fi
	    done
	fi
	%{_libexecdir}/%{name}/update_bacula_tables

	echo "If bacula works correctly you can remove the backup file /var/lib/%{name}/bacula_backup.sql.bz2"
fi
chown -R bacula:bacula /var/lib/%{name}
chmod -R u+rX,go-rwx /var/lib/%{name}
%endif

%if %{PGSQL}
%post dir-pgsql
umask 077
for f in create_postgresql_database drop_postgresql_database drop_postgresql_tables \
    grant_postgresql_privileges make_postgresql_tables update_postgresql_tables ; do
    ln -snf $f %{_libexecdir}/%{name}/${f/postgresql/bacula}
done
ln -snf bacula-dir-postgresql %{_sbindir}/bacula-dir
ln -snf bscan-postgresql %{_sbindir}/bscan
ln -snf dbcheck-postgresql %{_sbindir}/dbcheck
# NOTE: IF THIS FAILS DUE TO MYSQL/PGSQL NEEDING A PASSWORD YOU ARE ON YOUR OWN
DB_VER=`psql bacula -c 'select * from Version;' | tail -n 1 2>/dev/null`
if [ -z "$DB_VER" ]; then
	echo cannot connect to bacula catalog database
	echo if this is the first bacula installation please check
	echo and run the following scripts
	echo 	%{_libexecdir}/%{name}/grant_bacula_privileges
	echo 	%{_libexecdir}/%{name}/create_bacula_database
	echo 	%{_libexecdir}/%{name}/make_bacula_tables
	echo else manually update the database to version %{_cur_db_ver} using the script
	echo 	%{_libexecdir}/%{name}/update_bacula_tables
elif [ "$DB_VER" -lt "%{_cur_db_ver}" ]; then
	echo "Backing up bacula tables"
	pg_dump bacula | bzip2 > /var/lib/%{name}/bacula_backup.sql.bz2
	echo "Upgrading bacula tables"
	if [ "$DB_VER" -lt "7" ]; then
		echo "your bacula database version is too old to be upgraded automatically"
	else
	    for v in `seq 8 $((%{_cur_db_ver} - 1))`; do
		if [ "$DB_VER" -lt "$v" ]; then
			%{_libexecdir}/%{name}/update_postgresql_tables_$((v - 1))_to_$v
		fi
	    done
	fi
	%{_libexecdir}/%{name}/update_bacula_tables

	echo "If bacula works correctly you can remove the backup file /var/lib/%{name}/bacula_backup.sql.bz2"
fi
chown -R bacula:bacula /var/lib/%{name}
chmod -R u+rX,go-rwx /var/lib/%{name}
%endif

%if %{SQLITE3}
%post dir-sqlite3
umask 077
for f in create_sqlite3_database drop_sqlite3_database drop_sqlite3_tables \
    grant_sqlite3_privileges make_sqlite3_tables update_sqlite3_tables ; do
    ln -snf $f %{_libexecdir}/%{name}/${f/sqlite3/bacula}
done
ln -snf bacula-dir-sqlite3 %{_sbindir}/bacula-dir
ln -snf bscan-sqlite3 %{_sbindir}/bscan
ln -snf dbcheck-sqlite3 %{_sbindir}/dbcheck
[ -s /var/lib/%{name}/bacula.db ] && \
	DB_VER=`echo "select * from Version;" | \
		sqlite3 /var/lib/%{name}/bacula.db | tail -n 1 2>/dev/null`
if [ -z "$DB_VER" ]; then
# grant privileges and create tables
	%{_libexecdir}/%{name}/grant_bacula_privileges > dev/null
	%{_libexecdir}/%{name}/create_bacula_database > dev/null
	%{_libexecdir}/%{name}/make_bacula_tables > dev/null
elif [ "$DB_VER" -lt "%{_cur_db_ver}" ]; then
	echo "Backing up bacula tables"
	echo ".dump" | sqlite3 /var/lib/%{name}/bacula.db | bzip2 > /var/lib/%{name}/bacula_backup.sql.bz2
	echo "Upgrading bacula tables"
	if [ "$DB_VER" -lt "8" ]; then
		echo "your bacula database version is too old to be upgraded automatically"
	else
	    for v in `seq 9 $((%{_cur_db_ver} - 1))`; do
		if [ "$DB_VER" -lt "$v" ]; then
			%{_libexecdir}/%{name}/update_sqlite3_tables_$((v - 1))_to_$v
		fi
	    done
	fi
	%{_libexecdir}/%{name}/update_bacula_tables

	echo "If bacula works correctly you can remove the backup file /var/lib/%{name}/bacula_backup.sql.bz2"
fi
chown -R bacula:bacula /var/lib/%{name}
chmod -R u+rX,go-rwx /var/lib/%{name}
%endif

%post dir-sqlite
umask 077
for f in create_sqlite_database drop_sqlite_database drop_sqlite_tables \
    grant_sqlite_privileges make_sqlite_tables update_sqlite_tables ; do
    ln -snf $f %{_libexecdir}/%{name}/${f/sqlite/bacula}
done
ln -snf bacula-dir-sqlite %{_sbindir}/bacula-dir
ln -snf bscan-sqlite %{_sbindir}/bscan
ln -snf dbcheck-sqlite %{_sbindir}/dbcheck
[ -s /var/lib/%{name}/bacula.db ] && \
	DB_VER=`echo "select * from Version;" | \
		sqlite /var/lib/%{name}/bacula.db | tail -n 1 2>/dev/null`
if [ -z "$DB_VER" ]; then
# grant privileges and create tables
	%{_libexecdir}/%{name}/grant_bacula_privileges > dev/null
	%{_libexecdir}/%{name}/create_bacula_database > dev/null
	%{_libexecdir}/%{name}/make_bacula_tables > dev/null
elif [ "$DB_VER" -lt "%{_cur_db_ver}" ]; then
	echo "Backing up bacula tables"
	echo ".dump" | sqlite /var/lib/%{name}/bacula.db | bzip2 > /var/lib/%{name}/bacula_backup.sql.bz2
	echo "Upgrading bacula tables"
	if [ "$DB_VER" -lt "4" ]; then
		echo "your bacula database version is too old to be upgraded automatically"
	else
	    for v in `seq 5 $((%{_cur_db_ver} - 1))`; do
		if [ "$DB_VER" -lt "$v" ]; then
			%{_libexecdir}/%{name}/update_sqlite_tables_$((v - 1))_to_$v
		fi
	    done
	fi
	%{_libexecdir}/%{name}/update_bacula_tables

	echo "If bacula works correctly you can remove the backup file /var/lib/%{name}/bacula_backup.sql.bz2"
fi
chown -R bacula:bacula /var/lib/%{name}
chmod -R u+rX,go-rwx /var/lib/%{name}

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
if [ -e %{_sysconfdir}/%{name}/console.conf -a ! -e %{_sysconfdir}/%{name}/bconsole.conf ]; then
    mv %{_sysconfdir}/%{name}/console.conf %{_sysconfdir}/%{name}/bconsole.conf
fi

%post console
%post_fix_config bconsole

%if %{GNOME}
%post console-gnome
%post_fix_config gnome-console
%update_menus
		
%postun console-gnome
%clean_menus
%endif

%if %{WXWINDOWS}
%pre console-wx
if [ -e %{_sysconfdir}/%{name}/wx-console.conf -a ! -e %{_sysconfdir}/%{name}/bwx-console.conf ]; then
    mv %{_sysconfdir}/%{name}/wx-console.conf %{_sysconfdir}/%{name}/bwx-console.conf
fi

%post console-wx
%post_fix_config wx-console
%update_menus
		
%postun console-wx
%clean_menus
%endif

%if %{BAT}
%post bat
%post_fix_config bat
%update_menus
		
%postun bat
%clean_menus
%endif

%if %{TRAY}
%post tray-monitor
%post_fix_config tray-monitor
%update_menus
		
%postun tray-monitor
%clean_menus
%endif

%post -n nagios-check_bacula
%{_initrddir}/nagios condrestart > /dev/null 2>&1 || :

%postun -n nagios-check_bacula
if [ "$1" = "0" ]; then
    %{_initrddir}/nagios condrestart > /dev/null 2>&1 || :
fi

%clean
rm -rf %{buildroot}

%files common
%defattr(0644,root,root,0755)
%doc LICENSE
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/scripts
%attr(0755,root,root) %{_sbindir}/btraceback
%attr(0755,root,root) %{_sbindir}/bsmtp
%attr(0755,root,root) %{_sbindir}/bregex
%attr(0755,root,root) %{_sbindir}/bwild
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/btraceback.gdb
%{_libexecdir}/%{name}/btraceback.dbx
# i think this should go into %{name}-sd
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/%{name}/scripts/dvd-handler
%attr(770, %{name}, %{name}) %dir /var/lib/%{name}
%{_mandir}/man1/bsmtp.1*
%{_mandir}/man8/%{name}.8*
%{_mandir}/man8/btraceback.8*
%exclude %{_libexecdir}/%{name}/%{name}
%if ! %{GNOME}
%exclude %{_mandir}/man1/%{name}-console-gnome.1*
%endif
%if ! %{TRAY}
%exclude %{_mandir}/man1/%{name}-tray-monitor.1*
%endif
%if ! %{WXWINDOWS}
%exclude %{_mandir}/man1/%{name}-wxconsole.1*
%endif
%if %{BAT}
%exclude %{_mandir}/man1/%{name}-bat.1*
%endif

%files dir-common
%defattr(0644,root,root,0755)
%doc ChangeLog CheckList ReleaseNotes kernstodo LICENSE
# FIXME : Merge baculs-docs and use it
#%doc doc/*.pdf doc/manual examples
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}-dir.conf
%ghost %{_sysconfdir}/%{name}/.pw.sed
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}-dir
%{_mandir}/man8/%{name}-dir.8*
%{_mandir}/man8/dbcheck.8*
%{_mandir}/man8/bscan.8*
%defattr (0755,root,root)
%attr(0755,root,root) %{_initrddir}/%{name}-dir
%ghost %{_sbindir}/%{name}-dir
%ghost %{_sbindir}/dbcheck
%ghost %{_sbindir}/bscan
%ghost %{_libexecdir}/%{name}/create_%{name}_database
%ghost %{_libexecdir}/%{name}/drop_%{name}_database
%ghost %{_libexecdir}/%{name}/drop_%{name}_tables
%ghost %{_libexecdir}/%{name}/grant_%{name}_privileges
%ghost %{_libexecdir}/%{name}/make_%{name}_tables
%ghost %{_libexecdir}/%{name}/update_%{name}_tables
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/%{name}/scripts/make_catalog_backup
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/%{name}/scripts/delete_catalog_backup
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/scripts/query.sql
%exclude %{_libexecdir}/%{name}/%{name}-ctl-dir

%files dir-sqlite
%{_sbindir}/%{name}-dir-sqlite
%{_sbindir}/dbcheck-sqlite
%{_sbindir}/bscan-sqlite
%{_libexecdir}/%{name}/create_sqlite_database
%{_libexecdir}/%{name}/drop_sqlite_database
%{_libexecdir}/%{name}/drop_sqlite_tables
%{_libexecdir}/%{name}/grant_sqlite_privileges
%{_libexecdir}/%{name}/make_sqlite_tables
%{_libexecdir}/%{name}/update_sqlite_tables*

%if %{MYSQL}
%files dir-mysql
%{_sbindir}/%{name}-dir-mysql
%{_sbindir}/dbcheck-mysql
%{_sbindir}/bscan-mysql
%{_libexecdir}/%{name}/create_mysql_database
%{_libexecdir}/%{name}/drop_mysql_database
%{_libexecdir}/%{name}/drop_mysql_tables
%{_libexecdir}/%{name}/grant_mysql_privileges
%{_libexecdir}/%{name}/make_mysql_tables
%{_libexecdir}/%{name}/update_mysql_tables*
%endif

%if %{PGSQL}
%files dir-pgsql
%{_sbindir}/%{name}-dir-postgresql
%{_sbindir}/dbcheck-postgresql
%{_sbindir}/bscan-postgresql
%{_libexecdir}/%{name}/create_postgresql_database
%{_libexecdir}/%{name}/drop_postgresql_database
%{_libexecdir}/%{name}/drop_postgresql_tables
%{_libexecdir}/%{name}/grant_postgresql_privileges
%{_libexecdir}/%{name}/make_postgresql_tables
%{_libexecdir}/%{name}/update_postgresql_tables*
%endif

%if %{SQLITE3}
%files dir-sqlite3
%{_sbindir}/%{name}-dir-sqlite3
%{_sbindir}/dbcheck-sqlite3
%{_sbindir}/bscan-sqlite3
%{_libexecdir}/%{name}/create_sqlite3_database
%{_libexecdir}/%{name}/drop_sqlite3_database
%{_libexecdir}/%{name}/drop_sqlite3_tables
%{_libexecdir}/%{name}/grant_sqlite3_privileges
%{_libexecdir}/%{name}/make_sqlite3_tables
%{_libexecdir}/%{name}/update_sqlite3_tables*
%endif

%files fd
%defattr(0755,root,root)
%doc LICENSE
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}-fd.conf
%attr(0755,root,root) %{_initrddir}/%{name}-fd
%{_sbindir}/%{name}-fd
%attr(0644,root,root) %{_mandir}/man8/%{name}-fd.8*
%exclude %{_libexecdir}/%{name}/%{name}-ctl-fd

%files sd
%defattr(0755,root,root)
%doc LICENSE
%attr(0755,root,root) %{_initrddir}/%{name}-sd
%dir %{_sysconfdir}/%{name}
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}-sd.conf
%{_sbindir}/%{name}-sd
%{_sbindir}/bcopy
%{_sbindir}/bextract
%{_sbindir}/bls
%{_sbindir}/btape
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/%{name}/scripts/mtx-changer
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/%{name}/scripts/disk-changer
%defattr(0644,root,root,0755)
%{_mandir}/man8/%{name}-sd.8*
%{_mandir}/man8/bcopy.8*
%{_mandir}/man8/bextract.8*
%{_mandir}/man8/bls.8*
%{_mandir}/man8/btape.8*
%exclude %{_libexecdir}/%{name}/%{name}-ctl-sd

%files console
%defattr(0644,root,root,0755)
%doc LICENSE
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/bconsole.conf
%config(noreplace) %{_sysconfdir}/security/console.apps/bconsole
%config(noreplace) %{_sysconfdir}/pam.d/bconsole
%attr(0755,root,root) %{_sbindir}/bconsole
%verify(link) %{_bindir}/bconsole
%{_mandir}/man8/bconsole.8*
%attr(0755,root,root) %{_libdir}/%{name}/bconsole
%exclude %{_libexecdir}/%{name}/bconsole

%if %{GNOME}
%files console-gnome
%defattr(0644,root,root,0755)
%doc LICENSE
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/bgnome-console.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/security/console.apps/bgnome-console
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/bgnome-console
%attr(0755,root,root) %{_sbindir}/bgnome-console
%verify(link) %{_bindir}/bgnome-console
%if %{mdkversion} <= 200700
%{_menudir}/%{name}-console-gnome
%endif
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}-console-gnome.desktop
%{_mandir}/man1/%{name}-bgnome-console.1*
%endif

%if %{WXWINDOWS}
%files console-wx
%defattr(0644,root,root,0755)
%doc LICENSE
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/bwx-console.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/security/console.apps/bwx-console
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/bwx-console
%attr(0755,root,root) %{_sbindir}/bwx-console
%verify(link) %{_bindir}/bwx-console
%if %{mdkversion} <= 200700
%{_menudir}/%{name}-console-wx
%endif
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}-console-wx.desktop
%{_mandir}/man1/%{name}-bwxconsole.1*
%endif

%if %{BAT}
%files bat
%defattr(0644,root,root,0755)
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/bat.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/security/console.apps/%{name}-bat
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/%{name}-bat
%attr(0755,root,root) %{_sbindir}/%{name}-bat
%verify(link) %{_bindir}/%{name}-bat
%if %{mdkversion} <= 200700
%{_menudir}/%{name}-bat
%endif
%{_iconsdir}/%{name}-bat.png
%{_miconsdir}/%{name}-bat.png
%{_liconsdir}/%{name}-bat.png
%{_datadir}/applications/mandriva-%{name}-bat.desktop
%{_mandir}/man1/%{name}-bat.1*
%endif

%if %{GUI}
%files gui-web
/var/www/html/%{name}/*
%dir %attr(0755,apache,apache) %{_sysconfdir}/%{name}/%{name}-web
%attr(0640,apache,apache) %config(noreplace) %{_sysconfdir}/%{name}/%{name}-web/%{name}.conf
%dir %attr(0755,apache,apache) /var/cache/httpd/%{name}-web

%files gui-bimagemgr
/var/www/html/bimagemgr/*.gif
/var/www/html/bimagemgr/*.html
/var/www/cgi-bin/bimagemgr.pl
%{_sysconfdir}/create_cdimage_table.pl
%endif

%if %{TRAY}
%files tray-monitor
%defattr(0644,root,root,0755)
%doc LICENSE
%config(noreplace) %{_sysconfdir}/%{name}/tray-monitor.conf
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}-tray-monitor
%config(noreplace) %{_sysconfdir}/pam.d/%{name}-tray-monitor
%{_sbindir}/%{name}-tray-monitor
%verify(link) %{_bindir}/%{name}-tray-monitor
%if %{mdkversion} <= 200700
%{_menudir}/%{name}-tray-monitor
%endif
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}-tray-monitor.desktop
%{_mandir}/man1/%{name}-tray-monitor.1*
%endif

%files -n nagios-check_bacula
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/nagios/plugins.d/check_bacula.cfg
%{_libdir}/nagios/plugins/check_bacula
