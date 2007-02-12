Summary:	GPG-Ezmlm encrypted mailing list
Summary(pl.UTF-8):   GPG-Ezmlm - szyfrowana lista dyskusyjna
Name:		gpg-ezmlm
Version:	0.3.2
Release:	0.8
Epoch:		0
License:	BSD
Group:		Applications/Mail
Source0:	http://www.synacklabs.net/projects/crypt-ml/%{name}-%{version}.tar.gz
# Source0-md5:	4541a06a407a74dd1110c62a8fdef484
Patch0:		%{name}-fixes.patch
URL:		http://www.synacklabs.net/projects/crypt-ml/
BuildRequires:	rpmbuild(macros) >= 1.194
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	sed >= 4.0
Requires:	gnupg
# requires actually just ezmlm.
Requires:	ezmlm-idx
Requires:	qmail
Requires:	perl-Digest-MD5
Requires:	perl-File-Sync
Requires:	perl-base
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GPG-Ezmlm is an encrypted mailing list. PGP or GPG encrypted mails
sent to the list are re-encrypted with subscriber keys, allowing for
encrypted mail communications without requiring that all users know
all other users' keys. Key exchange during list subscription is
supported. It requires an existing Ezmlm installation to function.

%description -l pl.UTF-8
GPG-Ezmlm to szyfrowana lista dyskusyjna. Listy zaszyfrowane PGP lub
GPG wysłane na listę są ponownie szyfrowane kluczami subskrybentów, co
pozwala na szyfrowaną komunikację bez potrzeby posiadania przez
wszystkich kluczy pozostałych użytkowników. Wymiana kluczy podczas
zapisywania na listę jest obsługiwana. Pakiet wymaga do działania
istniejącej instalacji Ezmlma.

%prep
%setup -q
%patch0 -p1
sed -i -e '1s,^.*bin/perl,#!%{__perl},' *.pl
sed -i -e 's,/usr/local/bin/gpg,%{_bindir}/gpg,' *.p[lm] config

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# duplicate
rm -rf $RPM_BUILD_ROOT%{perl_vendorlib}/*.pl

# regular nuking
rm -f $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/gpg-ezmlm/.packlist

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 = 1 ]; then
	%banner -e %{name} <<EOF
Read the bundled README how to use this package with ezmlm.
EOF
fi

%files
%defattr(644,root,root,755)
%doc LICENSE README TODO Changes
%attr(755,root,root) %{_bindir}/gpg-ezmlm-convert.pl
%attr(755,root,root) %{_bindir}/gpg-ezmlm-manage.pl
%attr(755,root,root) %{_bindir}/gpg-ezmlm-send.pl
%{perl_vendorlib}/GpgEzmlm.pm
%{_mandir}/man3/GpgEzmlm.3pm*
