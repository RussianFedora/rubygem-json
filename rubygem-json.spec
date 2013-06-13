%global gem_name json
%if 0%{?rhel} <= 6 && 0%{?fedora} <= 16
%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_cache %{gem_dir}/cache
%global gem_libdir %{gem_instdir}/lib
%global gem_extdir %{_libdir}/gems/exts/%{gem_name}-%{version}
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%global rubyabi 1.8
%else
%global rubyabi 1.9.1
%endif

Summary:       JSON Implementation for Ruby
Name:          rubygem-%{gem_name}
Version:       1.8.0
Release:       2%{?dist}
Group:         Development/Languages
License:       GPLv2+ or Ruby
URL:           http://flori.github.com/json
Source0:       http://rubygems.org/downloads/%{gem_name}-%{version}.gem
#_mx Patch0:        rubygem-json-CVE-2013-0269-denial-of-service.patch
Requires:      ruby(abi) = %{rubyabi}
Requires:      ruby(rubygems) 
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby-devel
BuildRequires: rubygems
%if 0%{?rhel} >= 7 && 0%{?fedora} >= 16
BuildRequires: rubygems-devel
%endif
Provides: rubygem(%{gem_name}) = %{version}

%description
This is a JSON implementation as a Ruby extension in C.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

#_mx %patch0 -p1

%build
mkdir -p ./%{gem_dir}
gem build %{gem_name}.gemspec

export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install -V \
        --local \
        --install-dir ./%{gem_dir} \
        --force \
        --rdoc \
        %{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p $RPM_BUILD_ROOT%{gem_extdir}/lib/%{gem_name}
mv .%{gem_libdir}/json/ext \
	$RPM_BUILD_ROOT%{gem_extdir}/lib/%{gem_name}

# We don't need those files anymore.
rm -rf $RPM_BUILD_ROOT%{gem_instdir}/ext
rm -rf $RPM_BUILD_ROOT%{gem_instdir}/install.rb
rm -rf $RPM_BUILD_ROOT%{gem_instdir}/{.require_paths,.gitignore,.travis.yml,.yardoc}
rm -rf $RPM_BUILD_ROOT%{gem_instdir}/lib/json/ext/
rm -rf $RPM_BUILD_ROOT%{gem_instdir}/diagrams
rm -rf $RPM_BUILD_ROOT%{gem_docdir}/rdoc/classes/*
rm -rf $RPM_BUILD_ROOT%{gem_docdir}/ri/*
rm -rf $RPM_BUILD_ROOT%{gem_instdir}/java/

%check
pushd .%{gem_instdir}
# copy .so files into proper places for testing
pushd ext/%{gem_name}/ext
cp parser/parser.so .
cp generator/generator.so .
popd
testrb -Ilib:ext tests/test_*
popd

%files
%doc %{gem_instdir}/[A-Z]*
%dir %{gem_instdir}
%{gem_instdir}/tools/
%{gem_libdir}
%{gem_extdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/Rakefile
%{gem_instdir}/data
%{gem_instdir}/tests
%{gem_instdir}/*gemspec
%doc %{gem_docdir}

%changelog
* Fri Jun 07 2013 Sergey Mihailov <sergey.mihailov@gmail.com> - 1.8.0-1
- Update release
- Drop patch : Fix for CVE-2013-0269

* Wed Feb 20 2013 Troy Dawson <tdawson@redhat.com> - 1.7.3-2
- Fix for CVE-2013-0269.

* Tue Oct 30 2012 Troy Dawson <tdawson@redhat.com> - 1.4.6-13
- Added rake-compiler for building

* Tue Oct 30 2012 Troy Dawson <tdawson@redhat.com> - 1.4.6-12
- Fixed patch so that it uses normal rpm patching methods

* Fri Feb 10 2012 Steve Linabery <slinaber@redhat.com> - 1.4.6-5
- remove files not included in spec files section

* Fri Feb 10 2012 Steve Linabery <slinaber@redhat.com> - 1.4.6-4
- Commented out *-gui subpackages to avoid dependency on ruby-gtk2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.4.6-2
- Rebuilt for gcc bug 634757

* Sat Sep 18 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.6-1
- Update release.
- Enabled test stage.

* Fri Jun 11 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-3
- Move ruby's site_lib editor to ruby-json-gui.

* Mon May 10 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-2
- Move editor out of ruby-json sub-package.

* Sun May 09 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-1
- Update release.
- Split-out json editor.

* Thu Oct 29 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.9-1
- Update release.

* Wed Aug 12 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-3
- Fix gem scripts and install_dir.
- Enable %%check stage.

* Wed Aug 05 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-2
- Rebuild in correct buildir process.
- Add sub packages.

* Mon Aug 03 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-1
- Update release.

* Sat Jun 06 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.6-1
- Update release.

* Tue May 12 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.5-1
- Update release.
 
* Thu Apr 02 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.4-1
- Update release.

* Sat Jul 12 2008 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.3-1
- Initial RPM release.


