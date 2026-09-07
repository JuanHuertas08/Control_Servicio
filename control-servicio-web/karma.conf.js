// Karma configuration. Adds a ChromeHeadlessNoSandbox launcher so tests
// can run in containerized/CI environments where Chrome must run as root.
module.exports = function (config) {
  config.set({
    customLaunchers: {
      ChromeHeadlessNoSandbox: {
        base: 'ChromeHeadless',
        flags: ['--no-sandbox', '--disable-gpu'],
      },
    },
  });
};
