Summary:	GNOME-DB widget library
Summary(pl):	Biblioteka widgetu GNOME-DB
Name:		libgnomedb
Version:	1.1.2
Release:	1
License:	LGPL
Group:		Applications/Databases
Source0:	ftp://ftp.gnome-db.org/pub/gnome-db/sources/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	015d3f329210b1420139c606839f9529
#Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/1.1/%{name}-%{version}.tar.bz2
Source1:	%{name}-fdl-appendix.sgml
Patch0:		%{name}-locale-names.patch
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	gtksourceview-devel
BuildRequires:	libgda-devel >= 1.1.2
Buildrequires:	libglade2-devel
BuildRequires:	libgnomeui-devel >= 2.4.0.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	scrollkeeper
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	scrollkeeper
Requires(post):	GConf2 >= 2.4.0.1
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
Requires:	%{name} = %{version}-%{release}
Requires:	gtksourceview-devel
Requires:	libgda-devel >= 1.1.2
Requires:	libgnomeui-devel >= 2.4.0.1

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
Requires:	%{name}-devel = %{version}-%{release}

%description static
GNOME-DB widget static libraries.

%description static -l pl
Statyczne biblioteki widgetu GNOME-DB.

%prep
%setup -q
%patch0 -p1

mv po/{no,nb}.po

install %{SOURCE1} doc/C/fdl-appendix.sgml

%build
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome2-macros
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
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

install $RPM_BUILD_ROOT%{_pixmapsdir}/libgnomedb/gnome-db.png $RPM_BUILD_ROOT%{_pixmapsdir}/gnome-db.png

install -d $RPM_BUILD_ROOT%{_datadir}/gnome/capplets
mv $RPM_BUILD_ROOT%{_datadir}/control-center-2.0/capplets/database-properties.desktop $RPM_BUILD_ROOT%{_datadir}/gnome/capplets/database-properties.desktop

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
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/libglade/2.0/*.so
%{_libdir}/libglade/2.0/*.la
%{_datadir}/gnome/capplets/*
%{_datadir}/mime-info/*
%{_datadir}/gnome-db
%{_omf_dest_dir}/%{name}
%{_pixmapsdir}/libgnomedb
%{_pixmapsdir}/gnome-db.png

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/libgnomedb
%{_pkgconfigdir}/*.pc
%{_gtkdocdir}/libgnomedb

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
