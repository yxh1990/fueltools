# -*- encoding: utf-8 -*-

Gem::Specification.new do |s|
  s.name = %q{mixlib-log}
  s.version = "1.4.1"

  s.required_rubygems_version = Gem::Requirement.new(">= 0") if s.respond_to? :required_rubygems_version=
  s.authors = ["Opscode, Inc."]
  s.date = %q{2012-06-08}
  s.email = %q{info@opscode.com}
  s.extra_rdoc_files = ["README.rdoc", "LICENSE", "NOTICE"]
  s.files = ["lib/mixlib/log.rb", "lib/mixlib/log/version.rb", "lib/mixlib/log/formatter.rb", "spec/spec_helper.rb", "spec/mixlib/log_spec.rb", "spec/mixlib/log/formatter_spec.rb", "Rakefile", ".gemtest", "mixlib-log.gemspec", "README.rdoc", "LICENSE", "NOTICE"]
  s.homepage = %q{http://www.opscode.com}
  s.require_paths = ["lib"]
  s.rubygems_version = %q{1.3.7}
  s.summary = %q{A gem that provides a simple mixin for log functionality}

  if s.respond_to? :specification_version then
    current_version = Gem::Specification::CURRENT_SPECIFICATION_VERSION
    s.specification_version = 3

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_development_dependency(%q<rake>, ["~> 0.9.2.2"])
      s.add_development_dependency(%q<rspec>, ["~> 2.10.0"])
      s.add_development_dependency(%q<cucumber>, ["~> 1.2.0"])
    else
      s.add_dependency(%q<rake>, ["~> 0.9.2.2"])
      s.add_dependency(%q<rspec>, ["~> 2.10.0"])
      s.add_dependency(%q<cucumber>, ["~> 1.2.0"])
    end
  else
    s.add_dependency(%q<rake>, ["~> 0.9.2.2"])
    s.add_dependency(%q<rspec>, ["~> 2.10.0"])
    s.add_dependency(%q<cucumber>, ["~> 1.2.0"])
  end
end
