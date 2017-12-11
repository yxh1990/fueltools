
# This file was created by mkconfig.rb when ruby was built.  Any
# changes made to this file will be lost the next time ruby is built.

module Config
  RUBY_VERSION == "1.8.7" or
    raise "ruby lib version (1.8.7) doesn't match executable version (#{RUBY_VERSION})"

  TOPDIR = File.dirname(__FILE__).chomp!("/lib64/ruby/1.8/x86_64-linux")
  DESTDIR = '' unless defined? DESTDIR
  CONFIG = {}
  CONFIG["DESTDIR"] = DESTDIR
  CONFIG["PATCHLEVEL"] = "352"
  CONFIG["INSTALL"] = '/usr/bin/install -c'
  CONFIG["EXEEXT"] = ""
  CONFIG["prefix"] = (TOPDIR || DESTDIR + "/usr")
  CONFIG["ruby_install_name"] = "ruby"
  CONFIG["RUBY_INSTALL_NAME"] = "ruby"
  CONFIG["RUBY_SO_NAME"] = "ruby"
  CONFIG["MANTYPE"] = "doc"
  CONFIG["NROFF"] = "/usr/bin/nroff"
  CONFIG["configure_args"] = " '--build=x86_64-redhat-linux-gnu' '--host=x86_64-redhat-linux-gnu' '--target=x86_64-redhat-linux-gnu' '--program-prefix=' '--prefix=/usr' '--exec-prefix=/usr' '--bindir=/usr/bin' '--sbindir=/usr/sbin' '--sysconfdir=/etc' '--datadir=/usr/share' '--includedir=/usr/include' '--libdir=/usr/lib64' '--libexecdir=/usr/libexec' '--localstatedir=/var' '--sharedstatedir=/var/lib' '--mandir=/usr/share/man' '--infodir=/usr/share/info' '--with-default-kcode=none' '--enable-shared' '--enable-pthread' '--disable-rpath' '--with-readline-include=/usr/include/readline5' '--with-readline-lib=/usr/lib64/readline5' '--enable-dtrace' '--with-sitedir=/usr/lib/ruby/site_ruby' '--with-sitearchdir=/usr/lib64/ruby/site_ruby' '--with-vendordir=/usr/lib/ruby' '--with-vendorarchdir=/usr/lib64/ruby' 'build_alias=x86_64-redhat-linux-gnu' 'host_alias=x86_64-redhat-linux-gnu' 'target_alias=x86_64-redhat-linux-gnu' 'CFLAGS=-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -fno-strict-aliasing'"
  CONFIG["vendorarchdir"] = "$(DESTDIR)/usr/lib64/ruby"
  CONFIG["sitearchdir"] = "$(DESTDIR)/usr/lib64/ruby/site_ruby"
  CONFIG["ruby_mm_version"] = "1.8"
  CONFIG["vendordir"] = "$(DESTDIR)/usr/lib/ruby"
  CONFIG["sitedir"] = "$(DESTDIR)/usr/lib/ruby/site_ruby"
  CONFIG["sitearch"] = "x86_64-linux"
  CONFIG["arch"] = "x86_64-linux"
  CONFIG["MAKEFILES"] = "Makefile"
  CONFIG["EXPORT_PREFIX"] = ""
  CONFIG["COMMON_HEADERS"] = ""
  CONFIG["COMMON_MACROS"] = ""
  CONFIG["COMMON_LIBS"] = ""
  CONFIG["MAINLIBS"] = ""
  CONFIG["ENABLE_SHARED"] = "yes"
  CONFIG["DLDLIBS"] = " -lc"
  CONFIG["SOLIBS"] = "$(LIBS)"
  CONFIG["LIBRUBYARG_SHARED"] = "-l$(RUBY_SO_NAME)"
  CONFIG["LIBRUBYARG_STATIC"] = "-l$(RUBY_SO_NAME)-static"
  CONFIG["LIBRUBYARG"] = "$(LIBRUBYARG_SHARED)"
  CONFIG["LIBRUBY"] = "$(LIBRUBY_SO)"
  CONFIG["LIBRUBY_ALIASES"] = "lib$(RUBY_SO_NAME).so.$(MAJOR).$(MINOR) lib$(RUBY_SO_NAME).so"
  CONFIG["LIBRUBY_SO"] = "lib$(RUBY_SO_NAME).so.$(MAJOR).$(MINOR).$(TEENY)"
  CONFIG["LIBRUBY_A"] = "lib$(RUBY_SO_NAME)-static.a"
  CONFIG["RUBYW_INSTALL_NAME"] = ""
  CONFIG["rubyw_install_name"] = ""
  CONFIG["LIBRUBY_DLDFLAGS"] = "-Wl,-soname,lib$(RUBY_SO_NAME).so.$(MAJOR).$(MINOR)"
  CONFIG["LIBRUBY_LDSHARED"] = "$(CC) -shared"
  CONFIG["debugflags"] = ""
  CONFIG["optflags"] = ""
  CONFIG["cflags"] = "$(optflags) $(debugflags)"
  CONFIG["cppflags"] = ""
  CONFIG["RDOCTARGET"] = ""
  CONFIG["ARCHFILE"] = ""
  CONFIG["EXTOUT"] = ".ext"
  CONFIG["PREP"] = "miniruby$(EXEEXT)"
  CONFIG["setup"] = "Setup"
  CONFIG["EXTSTATIC"] = ""
  CONFIG["STRIP"] = "strip -S -x"
  CONFIG["TRY_LINK"] = ""
  CONFIG["LIBPATHENV"] = "LD_LIBRARY_PATH"
  CONFIG["RPATHFLAG"] = ""
  CONFIG["LIBPATHFLAG"] = " -L%s"
  CONFIG["LINK_SO"] = ""
  CONFIG["LIBEXT"] = "a"
  CONFIG["DLEXT2"] = ""
  CONFIG["DLEXT"] = "so"
  CONFIG["LDSHARED"] = "$(CC) -shared"
  CONFIG["CCDLFLAGS"] = " -fPIC"
  CONFIG["STATIC"] = ""
  CONFIG["ARCH_FLAG"] = ""
  CONFIG["DLDFLAGS"] = ""
  CONFIG["DTRACE_HEADER"] = "dtrace.h"
  CONFIG["ALLOCA"] = ""
  CONFIG["MAKEDIRS"] = "mkdir -p"
  CONFIG["CP"] = "cp"
  CONFIG["RM"] = "rm -f"
  CONFIG["INSTALL_DATA"] = "$(INSTALL) -m 644"
  CONFIG["INSTALL_SCRIPT"] = "$(INSTALL)"
  CONFIG["INSTALL_PROGRAM"] = "$(INSTALL)"
  CONFIG["SET_MAKE"] = ""
  CONFIG["LN_S"] = "ln -s"
  CONFIG["OBJDUMP"] = ""
  CONFIG["DLLWRAP"] = ""
  CONFIG["WINDRES"] = ""
  CONFIG["NM"] = ""
  CONFIG["ASFLAGS"] = ""
  CONFIG["AS"] = "as"
  CONFIG["AR"] = "ar"
  CONFIG["RANLIB"] = "ranlib"
  CONFIG["YFLAGS"] = ""
  CONFIG["YACC"] = "bison -y"
  CONFIG["OUTFLAG"] = "-o "
  CONFIG["CPPOUTFILE"] = "-o conftest.i"
  CONFIG["GNU_LD"] = "yes"
  CONFIG["EGREP"] = "/bin/grep -E"
  CONFIG["GREP"] = "/bin/grep"
  CONFIG["CPP"] = "gcc -E"
  CONFIG["OBJEXT"] = "o"
  CONFIG["CPPFLAGS"] = " $(DEFS) $(cppflags)"
  CONFIG["LDFLAGS"] = "-L.  -rdynamic -Wl,-export-dynamic"
  CONFIG["CFLAGS"] = "-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -fno-strict-aliasing  -fPIC $(cflags)"
  CONFIG["CC"] = "gcc"
  CONFIG["target_os"] = "linux"
  CONFIG["target_vendor"] = "redhat"
  CONFIG["target_cpu"] = "x86_64"
  CONFIG["target"] = "x86_64-redhat-linux-gnu"
  CONFIG["host_os"] = "linux-gnu"
  CONFIG["host_vendor"] = "redhat"
  CONFIG["host_cpu"] = "x86_64"
  CONFIG["host"] = "x86_64-redhat-linux-gnu"
  CONFIG["build_os"] = "linux-gnu"
  CONFIG["build_vendor"] = "redhat"
  CONFIG["build_cpu"] = "x86_64"
  CONFIG["build"] = "x86_64-redhat-linux-gnu"
  CONFIG["TEENY"] = "7"
  CONFIG["MINOR"] = "8"
  CONFIG["MAJOR"] = "1"
  CONFIG["target_alias"] = "x86_64-redhat-linux-gnu"
  CONFIG["host_alias"] = "x86_64-redhat-linux-gnu"
  CONFIG["build_alias"] = "x86_64-redhat-linux-gnu"
  CONFIG["LIBS"] = "-lpthread -lrt -ldl -lcrypt -lm "
  CONFIG["ECHO_T"] = ""
  CONFIG["ECHO_N"] = "-n"
  CONFIG["ECHO_C"] = ""
  CONFIG["DEFS"] = ""
  CONFIG["mandir"] = "$(DESTDIR)/usr/share/man"
  CONFIG["localedir"] = "$(datarootdir)/locale"
  CONFIG["libdir"] = "$(DESTDIR)/usr/lib64"
  CONFIG["psdir"] = "$(docdir)"
  CONFIG["pdfdir"] = "$(docdir)"
  CONFIG["dvidir"] = "$(docdir)"
  CONFIG["htmldir"] = "$(docdir)"
  CONFIG["infodir"] = "$(DESTDIR)/usr/share/info"
  CONFIG["docdir"] = "$(datarootdir)/doc/$(PACKAGE)"
  CONFIG["oldincludedir"] = "/usr/include"
  CONFIG["includedir"] = "$(DESTDIR)/usr/include"
  CONFIG["localstatedir"] = "$(DESTDIR)/var"
  CONFIG["sharedstatedir"] = "$(DESTDIR)/var/lib"
  CONFIG["sysconfdir"] = "$(DESTDIR)/etc"
  CONFIG["datadir"] = "$(DESTDIR)/usr/share"
  CONFIG["datarootdir"] = "$(prefix)/share"
  CONFIG["libexecdir"] = "$(DESTDIR)/usr/libexec"
  CONFIG["sbindir"] = "$(DESTDIR)/usr/sbin"
  CONFIG["bindir"] = "$(DESTDIR)/usr/bin"
  CONFIG["exec_prefix"] = "$(DESTDIR)/usr"
  CONFIG["PACKAGE_BUGREPORT"] = ""
  CONFIG["PACKAGE_STRING"] = ""
  CONFIG["PACKAGE_VERSION"] = ""
  CONFIG["PACKAGE_TARNAME"] = ""
  CONFIG["PACKAGE_NAME"] = ""
  CONFIG["PATH_SEPARATOR"] = ":"
  CONFIG["SHELL"] = "/bin/sh"
  CONFIG["ruby_version"] = "$(MAJOR).$(MINOR)"
  CONFIG["rubylibdir"]    = "$(vendordir)/$(ruby_version)"
  CONFIG["archdir"]       = "$(libdir)/ruby/$(ruby_version)/$(sitearch)"
  CONFIG["sitelibdir"]    = "$(sitedir)/$(ruby_version)"
  CONFIG["sitearchdir"]   = "$(libdir)/ruby/site_ruby/$(ruby_version)/$(sitearch)"
  CONFIG["vendorlibdir"]  = "$(vendordir)/$(ruby_version)"
  CONFIG["vendorarchdir"] = "$(libdir)/ruby/$(ruby_version)/$(sitearch)"
  CONFIG["topdir"] = File.dirname(__FILE__)
  MAKEFILE_CONFIG = {}
  CONFIG.each{|k,v| MAKEFILE_CONFIG[k] = v.dup}
  def Config::expand(val, config = CONFIG)
    val.gsub!(/\$\$|\$\(([^()]+)\)|\$\{([^{}]+)\}/) do |var|
      if !(v = $1 || $2)
	'$'
      elsif key = config[v = v[/\A[^:]+(?=(?::(.*?)=(.*))?\z)/]]
	pat, sub = $1, $2
	config[v] = false
	Config::expand(key, config)
	config[v] = key
	key = key.gsub(/#{Regexp.quote(pat)}(?=\s|\z)/n) {sub} if pat
	key
      else
	var
      end
    end
    val
  end
  CONFIG.each_value do |val|
    Config::expand(val)
  end
end
RbConfig = Config # compatibility for ruby-1.9
CROSS_COMPILING = nil unless defined? CROSS_COMPILING
