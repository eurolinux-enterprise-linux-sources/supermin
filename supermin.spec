Summary:       Tool for creating supermin appliances
Name:          supermin
Version:       4.1.4
Release:       1%{?dist}
License:       GPLv2+

%if 0%{?rhel} >= 7
ExclusiveArch: x86_64
%endif

URL:           http://people.redhat.com/~rjones/supermin/
Source0:       http://libguestfs.org/download/supermin/%{name}-%{version}.tar.gz

BuildRequires: /usr/bin/pod2man
BuildRequires: yum >= 3.2
BuildRequires: /usr/sbin/mke2fs
BuildRequires: e2fsprogs-devel
BuildRequires: glibc-static, zlib-static
BuildRequires: ocaml, ocaml-findlib-devel
BuildRequires: prelink

# automake isn't actually required; however the src/.depend file gets
# rebuilt which newer automake thinks (wrongly) means that the
# Makefile.am has been touched and needs rebuilding.
BuildRequires: automake

Requires:      yum >= 3.2
Requires:      yum-utils
Requires:      supermin-helper%{?_isa} = %{version}-%{release}

# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries#Packages_granted_exceptions
Provides:      bundled(gnulib)

# NB: Does NOT Provides, because this is not a compatible replacement.
Obsoletes:     febootstrap <= 3.21-1


%description
Supermin is a tool for building supermin appliances.  These are tiny
appliances (similar to virtual machines), usually around 100KB in
size, which get fully instantiated on-the-fly in a fraction of a
second when you need to boot one of them.


%package helper
Summary:       Runtime support for supermin
Requires:      util-linux-ng
Requires:      cpio
Requires:      /usr/sbin/mke2fs
# RHBZ#771310
Requires:      e2fsprogs-libs >= 1.42

# NB: Does NOT Provides, because this is not a compatible replacement.
Obsoletes:     febootstrap-supermin-helper <= 3.21-1


%description helper
%{name}-helper contains the runtime support for %{name}.


%prep
%setup -q


%build
%configure --disable-network-tests
make


%install
make DESTDIR=$RPM_BUILD_ROOT install

# supermin-helper is marked as requiring an executable stack.  This
# happens because we use objcopy to create one of the component object
# files from a data file.  The program does not in fact require an
# executable stack.  The easiest way to fix this is to clear the flag
# here.
execstack -c $RPM_BUILD_ROOT%{_bindir}/supermin-helper


%check
make check


%files
%doc COPYING README examples/build-basic-vm.sh
%{_bindir}/supermin
%{_mandir}/man8/supermin.8*


%files helper
%doc COPYING
%{_bindir}/supermin-helper
%{_mandir}/man8/supermin-helper.8*


%changelog
* Wed Aug 28 2013 Richard W.M. Jones <rjones@redhat.com> - 4.1.4-1
- New upstream version 4.1.4.
- Supports compressed cpio image files, experimentally.

* Fri Aug  9 2013 Richard W.M. Jones <rjones@redhat.com> - 4.1.3-1
- New upstream version 4.1.3.
- Remove patch which is now upstream.
- Add examples directory to documentation.

* Tue Aug  6 2013 Richard W.M. Jones <rjones@redhat.com> - 4.1.2-2
- Include upstream patch to get correct directory setgid/sticky bits in
  the appliance.

* Sat Aug  3 2013 Richard W.M. Jones <rjones@redhat.com> - 4.1.2-1
- New upstream version 4.1.2.
- Remove patch which is now upstream.

* Wed Jun 26 2013 Richard W.M. Jones <rjones@redhat.com> - 4.1.1-2
- Add upstream patch to ignore ghost non-regular files.
- This fixes builds on Fedora 20 because the filesystem package has
  been changed so /var/lock and /var/run are marked as ghost.

* Tue Feb  5 2013 Richard W.M. Jones <rjones@redhat.com> - 4.1.1-1
- New upstream version 4.1.1.
- The program has been renamed 'supermin' from 'febootstrap'.
- Obsolete, but don't Provide because supermin is not a compatible replacement.
- Use '_isa' to specify architecture of supermin-helper subpackage.

* Tue Jan 22 2013 Richard W.M. Jones <rjones@redhat.com> - 1:3.21-2
- Add upstream patch to drop supplemental groups (RHBZ#902476).
- Remove 'Group:' RPM headers which are no longer necessary.
- Remove some commented-out requirements.

* Sat Dec 22 2012 Richard W.M. Jones <rjones@redhat.com> - 1:3.21-1
- New upstream version 3.21.

* Fri Aug 31 2012 Richard W.M. Jones <rjones@redhat.com> - 1:3.20-1
- New upstream version 3.20.

* Wed Aug 22 2012 Richard W.M. Jones <rjones@redhat.com> - 1:3.19-2
- Work around brokenness in yum (RHBZ#850913).
- Remove defattr, no longer required.

* Tue Jul 31 2012 Richard W.M. Jones <rjones@redhat.com> - 1:3.19-1
- New upstream version 3.19.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 Richard Jones <rjones@redhat.com> - 3.18-1
- New upstream version 3.18.
- This adds support for EPEL 5.

* Thu Jun 14 2012 Richard Jones <rjones@redhat.com> - 3.17-1
- New upstream version 3.17.

* Wed Jun 13 2012 Richard Jones <rjones@redhat.com> - 3.16-1
- New upstream version 3.16.

* Tue Jun 12 2012 Richard Jones <rjones@redhat.com> - 3.15-1
- New upstream version 3.15.
- This version includes root=<device> support, needed for libguestfs
  with virtio-scsi.
- Remove upstream patch.

* Thu May 17 2012 Richard Jones <rjones@redhat.com> - 3.14-6
- For RHEL 7 only, add ExclusiveArch x86-64.

* Tue May 15 2012 Richard Jones <rjones@redhat.com> - 3.14-5
- Bundled gnulib (RHBZ#821752).

* Fri Apr 13 2012 Richard Jones <rjones@redhat.com> - 3.14-4
- Add back explicit dependencies for external programs.

* Fri Apr 13 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.14-3
- Drop ExclusiveArch as it's supported on all primary & secondary arches
- Cleanup spec and deps

* Fri Mar 30 2012 Richard Jones <rjones@redhat.com> - 3.14-2
- New upstream version 3.14.
- Add upstream patch to fix RHBZ#808421.

* Thu Mar 29 2012 Richard Jones <rjones@redhat.com> - 3.13-4
- e2fsprogs moved /sbin/mke2fs to /usr/sbin (thanks Eric Sandeen).

* Thu Mar  1 2012 Richard Jones <rjones@redhat.com> - 3.13-2
- Missing BR zlib-static.

* Thu Feb  9 2012 Richard Jones <rjones@redhat.com> - 3.13-1
- New upstream version 3.13.
- Remove upstream patch which is included in this version.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan  3 2012 Richard Jones <rjones@redhat.com> - 3.12-4
- Depend on latest e2fsprogs (RHBZ#771310).

* Wed Nov  9 2011 Richard Jones <rjones@redhat.com> - 3.12-2
- Include upstream patch to work around Python stupidity.

* Tue Oct 18 2011 Richard Jones <rjones@redhat.com> - 3.12-1
- New upstream version 3.12.
- Remove upstream patch which is included in this version.

* Fri Oct 14 2011 Richard Jones <rjones@redhat.com> - 3.11-2
- Add upstream patch to fix febootstrap on non-Debian.

* Fri Oct 14 2011 Richard Jones <rjones@redhat.com> - 3.11-1
- New upstream version 3.11.

* Thu Sep  1 2011 Richard Jones <rjones@redhat.com> - 3.10-1
- New upstream version 3.10.

* Fri Aug 26 2011 Richard Jones <rjones@redhat.com> - 3.9-1
- New upstream version 3.9.

* Tue Jul 26 2011 Richard Jones <rjones@redhat.com> - 3.8-1
- New upstream version 3.8.

* Fri Jul 15 2011 Richard Jones <rjones@redhat.com> - 3.7-1
- New upstream version 3.7.

* Wed Jun  1 2011 Richard Jones <rjones@redhat.com> - 3.6-1
- New upstream version 3.6.
- This version no longer needs external insmod.static.

* Fri May 27 2011 Richard Jones <rjones@redhat.com> - 3.5-1
- New upstream version 3.5.
- Remove patch which is now upstream.

* Fri Mar 18 2011 Richard Jones <rjones@redhat.com> - 3.4-2
- Don't fail if objects are created in a symlinked dir (RHBZ#698089).

* Fri Mar 18 2011 Richard Jones <rjones@redhat.com> - 3.4-1
- New upstream version 3.4.
- febootstrap-supermin-helper Obsoletes older versions of febootstrap.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Richard Jones <rjones@redhat.com> - 3.3-4
- Split package into febootstrap (for building) and febootstrap-supermin-helper
  (for running).  Note that febootstrap depends on febootstrap-supermin-helper,
  but you can install febootstrap-supermin-helper on its own.

* Fri Jan 14 2011 Richard Jones <rjones@redhat.com> - 3.3-3
- Clear executable stack flag on febootstrap-supermin-helper.

* Thu Jan 13 2011 Dan Horák <dan[at]danny.cz> - 3.3-2
- add the ocaml's ExclusiveArch

* Sat Dec 11 2010 Richard Jones <rjones@redhat.com> - 3.3-1
- New upstream version 3.3.

* Tue Dec  7 2010 Richard Jones <rjones@redhat.com> - 3.2-1
- New upstream version 3.2.
- Remove upstream patches.

* Tue Dec  7 2010 Richard Jones <rjones@redhat.com> - 3.1-5
- Previous fix for RHBZ#654638 didn't work, fix it correctly.

* Mon Dec  6 2010 Richard Jones <rjones@redhat.com> - 3.1-4
- Properly ignore .*.hmac files (accidental reopening of RHBZ#654638).

* Mon Dec  6 2010 Richard Jones <rjones@redhat.com> - 3.1-3
- Uses yumdownloader at runtime, so require yum-utils.

* Mon Dec  6 2010 Richard Jones <rjones@redhat.com> - 3.1-2
- New upstream version 3.1.
- BR insmod.static.

* Sun Dec  5 2010 Richard Jones <rjones@redhat.com> - 3.0-2
- New upstream version 3.0 (note this is incompatible with 2.x).
- Fix upstream URLs.
- fakeroot, fakechroot no longer required.
- insmod.static is required at runtime (missing dependency from earlier).
- The only programs are 'febootstrap' and 'febootstrap-supermin-helper'.
- BR ocaml, ocaml-findlib-devel.
- No examples are provided with this version of febootstrap.

* Thu Nov 25 2010 Richard Jones <rjones@redhat.com> - 2.11-1
- New upstream version 2.11.
- Fixes "ext2fs_mkdir .. No free space in directory" bug which affects
  libguestfs on rawhide.

* Thu Oct 28 2010 Richard Jones <rjones@redhat.com> - 2.10-1
- New upstream version 2.10.
- Adds -u and -g options to febootstrap-supermin-helper which are
  required by virt-v2v.

* Fri Aug 27 2010 Richard Jones <rjones@redhat.com> - 2.9-1
- New upstream version 2.9.
- Fixes directory ordering problem in febootstrap-supermin-helper.

* Tue Aug 24 2010 Richard Jones <rjones@redhat.com> - 2.8-1
- New upstream version 2.8.

* Sat Aug 21 2010 Richard Jones <rjones@redhat.com> - 2.8-0.2
- New pre-release version of 2.8.
  + Note this is based on 2.7 + mailing list patches.
- New BRs on mke2fs, libext2fs, glibc-static.

* Fri May 14 2010 Richard Jones <rjones@redhat.com> - 2.7-2
- New upstream version 2.7.
- febootstrap-supermin-helper shell script rewritten in C for speed.
- This package contains C code so it is no longer 'noarch'.
- MAKEDEV isn't required.

* Fri Jan 22 2010 Richard Jones <rjones@redhat.com> - 2.6-1
- New upstream release 2.6.
- Recheck package in rpmlint.

* Thu Oct 22 2009 Richard Jones <rjones@redhat.com> - 2.5-2
- New upstream release 2.5.
- Remove BR upx (not needed by upstream).
- Two more scripts / manpages.

* Thu Jul 30 2009 Richard Jones <rjones@redhat.com> - 2.4-1
- New upstream release 2.4.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 15 2009 Richard Jones <rjones@redhat.com> - 2.3-1
- New upstream release 2.3.

* Mon Jun 15 2009 Richard Jones <rjones@redhat.com> - 2.2-1
- New upstream release 2.2.

* Mon May 11 2009 Richard Jones <rjones@redhat.com> - 2.0-1
- New upstream release 2.0.

* Thu May  7 2009 Richard Jones <rjones@redhat.com> - 1.9-1
- New upstream release 1.9.

* Fri May  1 2009 Richard Jones <rjones@redhat.com> - 1.8-1
- New upstream release 1.8.

* Mon Apr 20 2009 Richard Jones <rjones@redhat.com> - 1.7-1
- New upstream release 1.7.

* Tue Apr 14 2009 Richard Jones <rjones@redhat.com> - 1.5-3
- Configure script has (unnecessary) BuildRequires on fakeroot,
  fakechroot, yum.

* Tue Apr 14 2009 Richard Jones <rjones@redhat.com> - 1.5-2
- Initial build for Fedora.
