function responseWrapper(req, res, next) {
    const oldJson = res.json;
  
    res.json = function (data) {
      // If it's already wrapped, don't double-wrap it
      if (data && (data.status === 'okay' || data.status === 'error')) {
        return oldJson.call(this, data);
      }
  
      return oldJson.call(this, {
        status: 'okay',
        data: data
      });
    };
  
    next();
  }
  
  module.exports = responseWrapper;