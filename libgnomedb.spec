Summary:	GNOME-DB widget library
Summary(pl):	Biblioteka widgetu GNOME-DB
Name:		libgnomedb
Version:	0.91.0
Release:	1
License:	LGPL
Group:		Applications/Databases
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/0.91/%{name}-%{version}.tar.bz2
# Source0-md5:	bbbe32ea9d8deaa0c77bf1cfbeb5849d
BuildRequires:	gettext-devel
BuildRequires:	gnome-vfs2-devel
BuildRequires:	gtk-doc
# compilation fails with current gtksourceview (wait for new libgnomedb)
#BuildRequires:	gtksourceview-devel
BuildRequires:	libgda-devel >= 0.91.0
BuildRequires:	libgnomeui-devel >= 2.3.3.1-2
BuildRequires:	pkgconfig
BuildRequires:	scrollkeeper
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	scrollkeeper
Requires(post):	GConf2 >= 2.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libgnomedb is a library that eases the task of writing GNOME database
programs.

%description -l pl
libgnomedb jest bibliotek± u³atwiaj±c± pisanie programów bazodanowych.

%package devel
Summary:	GNOME-DB widget library development
Summary(pl):	Dla programistów widgetu GNOME-DB
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
libgnomedb is a library that eases the task of writing GNOME database
programs. This package contains development files.

%description devel -l pl
libgnomedb jest bibliotek± u³atwiaj±c± pisanie programów bazodanowych.
Ten podpakiet zawiera pliki dla programistów u¿ywaj±cych libgda.

%package static
Summary:	GNU Data Access static libraries
Summary(pl):	Statyczne biblioteki GNU Data Access
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
GNOME-DB widget static libraries.

%description static -l pl
Statyczne biblioteki widgetu GNOME-DB.

%prep
%setup -q

%build
rm -f missing
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome2-macros
%{__autoconf}
%{__automake}
%configure \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir} \
	pkgconfigdir=%{_pkgconfigdir} \
	omf_dest_dir=%{_omf_dest_dir}/%{name}

# no static modules
rm -f $RPM_BUILD_ROOT%{_libdir}/{bonobo/monikers,libglade/2.0}/*.a

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/usr/bin/scrollkeeper-update
%gconf_schema_install

%postun
/sbin/ldconfig
/usr/bin/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS
%{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/gnome-database-properties
%attr(755,root,root) %{_libdir}/gnome-database-components
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/bonobo/monikers/*.so
%{_libdir}/bonobo/monikers/*.la
%{_libdir}/bonobo/servers/*
%attr(755,root,root) %{_libdir}/libglade/2.0/*.so
%{_libdir}/libglade/2.0/*.la
%{_datadir}/control-center-2.0/capplets/*
%{_datadir}/mime-info/*
%{_datadir}/gnome-db
%{_omf_dest_dir}/%{name}
%{_pixmapsdir}/libgnomedb

%files devel
%defattr(644,root,root,755)
%doc %{_gtkdocdir}/libgnomedb
%{_includedir}/libgnomedb
%{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/lib*.so
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
