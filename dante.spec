%define major   0
%define libname_orig                            lib%{name}
%define libname                 %mklibname      %{name} %{major}
%define libnamedev              %mklibname      %{name} %{major} -d

#define _requires_exceptions GLIBC_PRIVATE

Summary:        A free Socks v4/v5 client implementation
Name:           dante
Version:        1.3.2
Release:        2
License:        BSD-like
Group:          Networking/Other
URL:            http://www.inet.no/dante/
Buildrequires:  perl-base pam-devel tcp_wrappers-devel
Source0:        http://www.inet.no/dante/files/%{name}-%{version}.tar.gz
Source1:        %{name}-sockd.init
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
Provides:       %{libname_orig}-devel = %{EVRD}
Provides:       %{name}-devel = %{EVRD}
Requires:       %{libname} = %{version}

%description -n %{libnamedev}
Additional libraries required to compile programs that use dante.

%package -n     %{libnamestaticdev}
Summary:        Static libraries for dante
Group:          Development/C
Provides:       %{libname_orig}-static-devel = %{EVRD}
Provides:       %{libname_orig}-static = %{EVRD}
Provides:       %{name}-static-devel = %{EVRD}
Provides:       %{name}-static = %{EVRD}

%description -n %{libnamestaticdev}
Static libraries for dante

%prep
%setup -q

%build
%configure2_5x --enable-shared --disable-static
%make

%install
%makeinstall

#perl -pi -e "s/libdl.so/`basename \`readlink %{_libdir}/libdl.so\``/;s/libdsocks.so/libdsocks.so.%major/" %{buildroot}%{_bindir}/socksify

install -m644 example/socks.conf -D %{buildroot}%{_sysconfdir}/socks.conf
install -m644 example/sockd.conf -D %{buildroot}%{_sysconfdir}/sockd.conf

install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/sockd
install -d %{buildroot}%{_sysconfdir}/sysconfig
cat <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/sockd
# Any extra option to pass to sockd
SOCKD_EXTRA_OPTIONS=
EOF

chmod +x %{buildroot}%{_libdir}/lib*.so*

%post server
%_post_service sockd

%preun server
%_preun_service sockd

%files
%doc BUGS CREDITS LICENSE NEWS README SUPPORT VERSION
%doc doc/README* doc/*.protocol doc/rfc*
%{_bindir}/socksify
%{_mandir}/man1/socksify.1*
%{_mandir}/man5/socks.conf.5*
%config(noreplace) %{_sysconfdir}/socks.conf

%files -n %{libname}
%{_libdir}/*.so.*

%files server
%{_sbindir}/sockd
%{_mandir}/man5/sockd.conf.5*
%{_mandir}/man8/*
%attr(0755,root,root) %{_initrddir}/sockd
%config(noreplace) %{_sysconfdir}/sockd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/sockd

%files -n %{libnamedev}
%{_libdir}/*.so
%{_includedir}/*.h




%changelog
* Wed Jul 23 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.1.19-7mdv2009.0
+ Revision: 243959
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 1.1.19-5mdv2008.1
+ Revision: 136360
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Mon May 28 2007 Bogdano Arendartchuk <bogdano@mandriva.com> 1.1.19-5mdv2008.0
+ Revision: 32136
- filter out GLIBC_PRIVATE automatic requires, should close #26910


* Fri Oct 27 2006 David Walluck <walluck@mandriva.org> 1.1.19-4mdv2007.0
+ Revision: 72930
- bunzip2 patches
- Import dante

* Tue Aug 15 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1.1.19-3mdv2007.0
- Fix rpmlint warnings

* Mon Jul 24 2006 Olivier Blin <blino@mandriva.com> 1.1.19-2mdv2007.0
- rebuild for new glibc

* Thu Mar 23 2006 Lenny Cartier <lenny@mandriva.com> 1.1.19-1mdk
- 1.1.19

* Thu Jul 21 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.1.17-1mdk
- New release 1.1.17
- mkrel

* Mon Jan 31 2005 Lenny Cartier <lenny@mandrakesoft.com> 1.1.15-1mdk
- 1.1.15

* Sat Jul 03 2004 Olivier Blin <blino@mandrake.org> 1.1.14-3mdk
- Patch0: redefine __GNUC__ for sys/wait.h inclusion
- move init script in init script directory

* Mon Jan 05 2004 Olivier Blin <blino@mandrake.org> 1.1.14-2mdk
- fix LD_PRELOAD in socksify script, ugly hack with readlink
  (is it 64bits-proof ?)
- require library in main package, find-requires doesn't find requires
  for LD_PRELOADs in shell scripts

* Sat Jan 03 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.1.14-1mdk
- 1.1.14
- cleanups!
- libify!

