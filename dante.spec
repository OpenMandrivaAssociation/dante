%define name    dante
%define version 1.1.19
%define release %mkrel 5
%define major   0
%define libname_orig                            lib%{name}
%define libname                 %mklibname      %{name} %{major}
%define libnamedev              %mklibname      %{name} %{major} -d
%define libnamestaticdev        %mklibname      %{name} %{major} -d -s

%define _requires_exceptions	GLIBC_PRIVATE

Summary:        A free Socks v4/v5 client implementation
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:        BSD-like
Group:          Networking/Other
URL:            http://www.inet.no/dante/
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Buildrequires:  perl-base pam-devel tcp_wrappers-devel
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}-sockd.init
Patch0:         %{name}-1.1.14-wait.patch
Patch1:         %{name}-1.1.12-pre1-pam-syslog.patch
Requires:       %{libname} = %{version}

%description
Dante is a free implementation of the proxy protocols socks version 4,
socks version 5 (rfc1928) and msproxy. It can be used as a firewall
between networks. It is being developed by Inferno Nettverk A/S, a
Norwegian consulting company. Commercial support is available.

This package contains the dynamic libraries required to "socksify"
existing applications to become socks clients.

%package        server
Summary:        A free Socks v4/v5 server implementation
Group:          System/Servers
Requires(pre):  rpm-helper

%package -n     %{libname}
Summary:        Library for Dante
Group:          System/Libraries

%description -n %{libname}
Library for Dante

%description    server
This package contains the socks proxy daemon and its documentation.
The sockd is the server part of the Dante socks proxy package and
allows socks clients to connect through it to the network.

%package -n     %{libnamedev}
Summary:        Development libraries for dante
Group:          Development/C
Provides:       %{libname_orig}-devel = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Requires:       %{libname} = %{version}

%description -n %{libnamedev}
Additional libraries required to compile programs that use dante.

%package -n     %{libnamestaticdev}
Summary:        Static libraries for dante
Group:          Development/C
Provides:       %{libname_orig}-static-devel = %{version}-%{release}
Provides:       %{libname_orig}-static = %{version}-%{release}
Provides:       %{name}-static-devel = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description -n %{libnamestaticdev}
Static libraries for dante

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

perl -pi -e "s/libdl.so/`basename \`readlink %{_libdir}/libdl.so\``/;s/libdsocks.so/libdsocks.so.%major/" $RPM_BUILD_ROOT%{_bindir}/socksify

install -m644 example/socks.conf -D $RPM_BUILD_ROOT%{_sysconfdir}/socks.conf
install -m644 example/sockd.conf -D $RPM_BUILD_ROOT%{_sysconfdir}/sockd.conf

install -m755 %{SOURCE1} -D $RPM_BUILD_ROOT%{_initrddir}/sockd
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
cat <<EOF > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/sockd
# Any extra option to pass to sockd
SOCKD_EXTRA_OPTIONS=
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post server
%_post_service sockd

%preun server
%_preun_service sockd

%files
%defattr(-,root,root)
%doc BUGS CREDITS LICENSE NEWS README SUPPORT TODO VERSION
%doc doc/README* doc/SOCKS4.protocol doc/faq* doc/rfc*
%{_bindir}/socksify
%{_mandir}/man5/socks.conf.5*
%config(noreplace) %{_sysconfdir}/socks.conf

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files server
%defattr(-,root,root)
%{_sbindir}/sockd
%{_mandir}/man5/sockd.conf.5*
%{_mandir}/man8/*
%attr(0755,root,root) %{_initrddir}/sockd
%config(noreplace) %{_sysconfdir}/sockd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/sockd

%files -n %{libnamedev}
%defattr (-,root,root)
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*.h

%files -n %{libnamestaticdev}
%defattr (-,root,root)
%{_libdir}/*.a


