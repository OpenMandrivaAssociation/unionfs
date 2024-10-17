%define module unionfs
%define version 1.4
%define release	%mkrel 6

Summary: A Stackable Unification File System
Name: %{module}
Version: %{version}
Release: %{release}
Source0: http://download.filesystems.org/unionfs/OLD/unionfs-1.x/%{name}-%{version}.tar.gz
Source1: unionfs-dkms.conf
# from Mandriva kernel package
Patch0: fs-unionfs-1.4.patch
# do not trigger BUG() in notify_change when setting mode attributes
# rediffed from "[PATCH 4/7] unionfs: fix unionfs_create and unionfs_setattr to handle ATTR_KILL_S*ID"
Patch1: fs-unionfs-1.4-attr_mode_notify_change.patch
Patch2: fs-unionfs-1.4-security_hooks.patch
Patch3: fs-unionfs-1.4-noapparmor.patch
Patch4: fs-unionfs-wrap-current-fsgid-fsuid.patch
Patch5: fs-unionfs-dentry_open-credentials.patch
Patch6: fs-unionfs-atomic_long_t-f_count.patch
Patch7: fs-unionfs-use-current_umask-helper.patch
License: GPL
Group: System/Kernel and hardware
URL: https://www.filesystems.org/project-unionfs.html
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Unionfs is a Stackable Unification File System.
This project builds a stackable unification file system, which can
appear to merge the contents of several directories (branches), while
keeping their physical content separate. Unionfs is useful for unified
source tree management, merged contents of split CD-ROM, merged
separate software package directories, data grids, and more. Unionfs
allows any mix of read-only and read-write branches, as well as
insertion and deletion of branches anywhere in the fan-out. To
maintain unix semantics, Unionfs handles elimination of duplicates,
partial-error conditions, and more. Unionfs is part of the larger FiST
project.

%package -n dkms-%{name}
Group: System/Kernel and hardware
Summary: Dkms module for the unionfs module
Requires(post): dkms
Requires(preun): dkms

%description -n dkms-%{name}
Unionfs is a Stackable Unification File System.
This package contains the kernel module.

%prep
%setup -q -c -T
cp %PATCH0 unionfs.patch
patch -p3 < unionfs.patch || [ -f unionfs.h ]
%patch1 -p3 -b .attr_mode_notify_change
%patch2 -p3 -b .security_hooks
%patch3 -p3
%patch4 -p3
%patch5 -p3
%patch6 -p3
%patch7 -p3
perl -pi -e 's/\$\(CONFIG_UNION_FS\)/m/' Makefile
perl -p -e 's/\@VERSION@/%{version}/' < %{SOURCE1} > dkms.conf

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%{module}-%{version}.%{release}/
install -m 644 dkms.conf %{buildroot}/usr/src/%{module}-%{version}.%{release}/dkms.conf
tar c . | tar x -C %{buildroot}/usr/src/%{module}-%{version}.%{release}/

%clean
rm -rf %{buildroot}

%files -n dkms-%{name}
%defattr(-,root,root)
%attr(0755,root,root) /usr/src/%{module}-%{version}.%{release}/

%post -n dkms-%{name}
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m %{module} -v %{version}.%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{module} -v %{version}.%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{module} -v %{version}.%{release}

%preun -n dkms-%{name}
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{module} -v %{version}.%{release} --all
