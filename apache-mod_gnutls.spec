%define		mod_name	gnutls
%define 	apxs		/usr/sbin/apxs
Summary:	SSL v3, TLS 1.0 and TLS 1.1 encryption for Apache HTTPD
Summary(pl.UTF-8):	Szyfrowanie SSL v3, TLS 1.0 i TLS 1.1 dla serwera HTTP Apache
Name:		apache-mod_%{mod_name}
Version:	0.5.9
Release:	0.1
License:	Apache Group License
Group:		Networking/Daemons/HTTP
Source0:	http://www.outoforder.cc/downloads/mod_gnutls/mod_gnutls-%{version}.tar.bz2
# Source0-md5:	9b7050fb0dfec88225b15c821dfd26c4
Source1:	%{name}.conf
Source2:	%{name}-dhfile
Source3:	%{name}-rsafile
Patch0:		%{name}-libtool.patch
Patch1:		%{name}-paths.patch
URL:		http://www.outoforder.cc/projects/apache/mod_gnutls/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.42
BuildRequires:	apr_memcache-devel >= 0.7.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnutls-devel >= 2.10.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _pkglibdir      %(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

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
	--with-apxs=%{apxs} 

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/{conf.d,tls}}
install src/.libs/libmod_gnutls.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_gnutls.so
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/40_mod_gnutls.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/tls/dhfile
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/tls/rsafile

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	echo "Generating dhfile/rsafile - this may take some time..."
        d=/etc/httpd/tls
        [ -f "$d/dhfile" ] || /usr/bin/certtool --generate-dh-params --bits 1024 --outfile $d/dhfile
        [ -f "$d/rsafile" ] || /usr/bin/certtool --generate-privkey --bits 512 --outfile $d/rsafile
fi
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
	rm -f /etc/httpd/tls/{dhfile,rsafile}
fi

%files
%defattr(644,root,root,755)
%attr(750,root,root) %dir %{_sysconfdir}/tls
%dir %{_sysconfdir}/tls
%attr(640,root,root) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_gnutls.conf
%attr(755,root,root) %{_pkglibdir}/mod_gnutls.so
