Summary:	GNOME-DB widget library
Summary(pl.UTF-8):	Biblioteka widgetów GNOME-DB
Name:		libgnomedb
Version:	1.2.2
Release:	13
Epoch:		1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/libgnomedb/1.2/%{name}-%{version}.tar.bz2
# Source0-md5:	cf8b1eb3aa3e7b18f46bc9bc9335dca7
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-gtk-doc.patch
Patch2:		%{name}-glib.patch
URL:		http://www.gnome-db.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.8
BuildRequires:	docbook-dtd412-xml
BuildRequires:	GConf2-devel
# only checked for, not used
#BuildRequires:	evolution-data-server-devel >= 1.0
BuildRequires:	gettext-devel
BuildRequires:	gnome-common >= 2.12.0
BuildRequires:	gtk+2-devel >= 2:2.10.1
BuildRequires:	gtk-doc >= 1.7
BuildRequires:	gtksourceview-devel >= 1.7.2
BuildRequires:	intltool
BuildRequires:	libgda-devel >= 1:1.2.3
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libgnomeui-devel >= 2.16.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
Requires(post):	/sbin/ldconfig
Requires(post,preun):	GConf2 >= 2.14.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libgnomedb is a library that eases the task of writing GNOME database
programs.

%description -l pl.UTF-8
libgnomedb jest biblioteką ułatwiającą pisanie programów bazodanowych.

%package devel
Summary:	GNOME-DB widget library development
Summary(pl.UTF-8):	Dla programistów widgetu GNOME-DB
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	gtk+2-devel >= 2:2.10.1
Requires:	gtksourceview-devel >= 1.7.2
Requires:	libgda-devel >= 1:1.2.3
Requires:	libglade2-devel >= 1:2.6.0
Requires:	libgnomeui-devel >= 2.16.0

%description devel
libgnomedb is a library that eases the task of writing GNOME database
programs. This package contains development files.

%description devel -l pl.UTF-8
libgnomedb jest biblioteką ułatwiającą pisanie programów bazodanowych.
Ten podpakiet zawiera pliki dla programistów używających libgda.

%package static
Summary:	GNU Data Access static libraries
Summary(pl.UTF-8):	Statyczne biblioteki GNU Data Access
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
GNOME-DB widget static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki widgetu GNOME-DB.

%package apidocs
Summary:	libgnomedb API documentation
Summary(pl.UTF-8):	Dokumentacja API libgnomedb
Group:		Documentation
Requires(post,postun):	scrollkeeper
Requires:	gtk-doc-common

%description apidocs
libgnomedb API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libgnomedb.

%package -n gnome-database-access-properties
Summary:	Database access properties
Summary(pl.UTF-8):	Właściwości dostępu do baz danych
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n gnome-database-access-properties
Allows to configure database access properties in GNOME.

%description -n gnome-database-access-properties -l pl.UTF-8
Narzędzie pozwalające na konfigurację dostępu do baz danych w GNOME.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
	--enable-gnome \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	desktopdir=%{_desktopdir}

# no static modules and *.la for glade modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.{la,a}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

ln -sf %{_pixmapsdir}/libgnomedb/gnome-db.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/gnome-db.png

# obsolete(?)
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/mime-info

%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{sr@Latn,sr@latin}
# duplicate of nb with obsolete name
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install libgnomedb.schemas

%preun
%gconf_schema_uninstall libgnomedb.schemas

%postun	-p /sbin/ldconfig

%post apidocs
%scrollkeeper_update_post

%postun apidocs
%scrollkeeper_update_post

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS
%attr(755,root,root) %{_libdir}/libgnomedb-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnomedb-2.so.4
# libglade2 module (include it here as lib requires libglade2 anyway)
%attr(755,root,root) %{_libdir}/libglade/2.0/libgnomedb.so
# for libgnomedb
%{_datadir}/gnome-db
%{_pixmapsdir}/libgnomedb
%{_sysconfdir}/gconf/schemas/libgnomedb.schemas

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnomedb-2.so
%{_includedir}/libgnomedb-1.2
%{_pkgconfigdir}/libgnomedb.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgnomedb-2.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libgnomedb
%{_omf_dest_dir}/%{name}

%files -n gnome-database-access-properties
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gnome-database-properties
%{_desktopdir}/database-properties.desktop
%{_pixmapsdir}/gnome-db.png
