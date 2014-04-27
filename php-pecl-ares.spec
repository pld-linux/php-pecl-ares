%define		php_name	php%{?php_suffix}
%define		modname	ares
%define		status		beta
Summary:	%{modname} - asynchronous resolver
Summary(pl.UTF-8):	%{modname} - asynchroniczny resolver
Name:		%{php_name}-pecl-%{modname}
Version:	0.7.0
Release:	7
License:	BSD, revised
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	24ec2e3089246bab68d01af9c93a1dc7
Patch0:		php-pecl-%{modname}-tsrm.patch
URL:		http://pecl.php.net/package/ares/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	c-ares-devel
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Binding for the ares (MIT) or c-ares (CURL) library.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Dowiązania do biblioteki ares (MIT) lub c-ares (CURL).

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .
%patch0 -p2

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}

cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
