function addPayment(renter_id) {
  location.assign('/renter/'+renter_id+'/add_payment');
}

function addProperty() {
  location.assign('/add_property');
}

function addLease(property_id) {
  location.assign('/property/'+property_id+'/lease');
}

function addRenter() {
  location.assign('/add_renter');
}