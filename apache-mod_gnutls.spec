# TODO
# - with apr_memcache: http://www.outoforder.cc/projects/libs/apr_memcache
# - config file
%define		mod_name	gnutls
%define 	apxs		/usr/sbin/apxs
Summary:	SSL v3, TLS 1.0 and TLS 1.1 encryption for Apache HTTPD
Summary(pl.UTF-8):	Szyfrowanie SSL v3, TLS 1.0 i TLS 1.1 dla serwera HTTP Apache
Name:		apache-mod_%{mod_name}
Version:	0.2.0
Release:	0.1
License:	Apache Group License
Group:		Networking/Daemons
Source0:	http://www.outoforder.cc/downloads/mod_gnutls/mod_gnutls-%{version}.tar.bz2
# Source0-md5:	80ab766a7b9cfbb730e789032ff26d68
Patch0:		%{name}-libtool.patch
Patch1:		%{name}-no_certtool.patch
URL:		http://www.outoforder.cc/projects/apache/mod_gnutls/
BuildRequires:	apache-apxs
BuildRequires:	apache-devel >= 2.0.42
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnutls-devel >= 1.2.0
BuildRequires:	libtool
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _pkglibdir      %(%{apxs} -q LIBEXECDIR 2>/dev/null)

%description
mod_gnutls uses the GnuTLS library to provide SSL v3, TLS 1.0 and TLS
1.1 encryption for Apache HTTPD. It is similar to mod_ssl in purpose,
but does not use OpenSSL.

Features:
- Support for SSL v3, TLS 1.0 and TLS 1.1.
- Support for Server Name Indication
- Distributed SSL Session Cache via Memcached
- Local SSL Session Cache using DBM

%description -l pl.UTF-8
mod_gnutls używa biblioteki GnuTLS do obsługi szyfrowania SSL v3, TLS
1.0 i TLS 1.1 dla serwera HTTP Apache. Pod względem przeznaczenia jest
podobny do mod_ssl, ale nie używa biblioteki OpenSSL.

Możliwości:
- obsługa SSL v3, TLS 1.0 i TLS 1.1
- obsługa identyfikacji nazwy serwera (Server Name Indication)
- rozproszona pamięć podręczna sesji SSL poprzez Memcached
- lokalna pamięć podręczna sesji SSL korzystająca z DBM

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--with-apxs=%{apxs} \
	--with-libgnutls=%{_prefix} \
	--without-apr-memcache
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}
install src/.libs/libmod_gnutls.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_gnutls.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_pkglibdir}/*
