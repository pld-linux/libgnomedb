Summary:	GNOME-DB widget library
Summary(pl.UTF-8):   Biblioteka widgetu GNOME-DB
Name:		libgnomedb
Version:	1.9.100
Release:	7
License:	LGPL v2+
Group:		Applications/Databases
Source0:	http://ftp.gnome.org/pub/gnome/sources/libgnomedb/1.9/%{name}-%{version}.tar.bz2
# Source0-md5:	a98ac52f084b1b0abad6b2c53ec034cc
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-gnome.patch
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.8
BuildRequires:	gettext-devel
BuildRequires:	gnome-common >= 2.12.0
BuildRequires:	gtk+2-devel >= 2:2.10.0
BuildRequires:	gtk-doc >= 1.6
BuildRequires:	gtksourceview-devel >= 1.6.1
BuildRequires:	intltool
BuildRequires:	libgda-devel >= 1.9.100
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libgnomeui-devel >= 2.15.2
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_ld	(-Wl,)?--as-needed

%description
libgnomedb is a library that eases the task of writing GNOME database
programs.

%description -l pl.UTF-8
libgnomedb jest biblioteką ułatwiającą pisanie programów bazodanowych.

%package devel
Summary:	GNOME-DB widget library development
Summary(pl.UTF-8):   Dla programistów widgetu GNOME-DB
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtksourceview-devel >= 1.6.1
Requires:	libgda-devel >= 1.9.100
Requires:	libgnomeui-devel >= 2.15.2

%description devel
libgnomedb is a library that eases the task of writing GNOME database
programs. This package contains development files.

%description devel -l pl.UTF-8
libgnomedb jest biblioteką ułatwiającą pisanie programów bazodanowych.
Ten podpakiet zawiera pliki dla programistów używających libgda.

%package static
Summary:	GNU Data Access static libraries
Summary(pl.UTF-8):   Statyczne biblioteki GNU Data Access
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
GNOME-DB widget static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki widgetu GNOME-DB.

%package -n gnome-database-access-properties
Summary:	Database access properties
Summary(pl.UTF-8):   Właściwości dostępu do baz danych
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires(post,preun):	GConf2 >= 2.14.0
Requires(post,postun):	scrollkeeper
Requires:	gtk+2 >= 2:2.10.0

%description -n gnome-database-access-properties
Allows to configure database access properties in GNOME.

%description -n gnome-database-access-properties -l pl.UTF-8
Pozwala na konfigurację dostępu do baz danych w GNOME.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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
	HTML_DIR=%{_gtkdocdir} \
	desktopdir=%{_desktopdir} \
	omf_dest_dir=%{_omf_dest_dir}/%{name} \
	pkgconfigdir=%{_pkgconfigdir}

# no static modules and *.la for bonobo or glade modules
rm -f $RPM_BUILD_ROOT%{_libdir}/{bonobo/monikers,libglade/2.0}/*.{la,a}

ln -sf %{_pixmapsdir}/libgnomedb/gnome-db.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/gnome-db.png

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no
rm -rf $RPM_BUILD_ROOT%{_datadir}/mime-info
rm -f $RPM_BUILD_ROOT%{_libdir}/libgnomedb/plugins/*.{a,la}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post -n gnome-database-access-properties
%gconf_schema_install libgnomedb.schemas
%scrollkeeper_update_post

%preun -n gnome-database-access-properties
%gconf_schema_uninstall libgnomedb.schemas

%postun -n gnome-database-access-properties
%scrollkeeper_update_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%dir %{_libdir}/libgnomedb
%dir %{_libdir}/libgnomedb/plugins
%attr(755,root,root)%{_libdir}/libgnomedb/plugins/lib*.so*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/libgnomedb-1.9
%{_pkgconfigdir}/*.pc
%{_gtkdocdir}/libgnomedb

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n gnome-database-access-properties
%defattr(644,root,root,755)
%{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libglade/2.0/*.so
%{_desktopdir}/*
%{_datadir}/libgnomedb
%{_omf_dest_dir}/%{name}
%{_pixmapsdir}/libgnomedb
%{_pixmapsdir}/gnome-db.png
