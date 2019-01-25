pragma solidity ^0.4.21;

contract shipmentRecords {

    struct shipment {
        string waybill;
        string updated_at;
        string location;
        string status;
        string notes;
    }

    // shipment object
    // you can also declare it public to access it from outside contract
    // https://solidity.readthedocs.io/en/v0.4.24/contracts.html#visibility-and-getters
    shipment shipment_obj;


    // set shipment public function
    // This is similar to persisting object in db.
    function setShipment(string waybill, string updated_at, string location, string status, string notes) public {
        shipment_obj = shipment({
            waybill : waybill, updated_at : updated_at, location : location, status : status, notes : notes

            });
    }

    // get user public function
    // This is similar to getting object from db.
    function getShipment() public returns (string, string, string, string, string) {
        return (
            shipment_obj.waybill, shipment_obj.updated_at, shipment_obj.location, shipment_obj.status, shipment_obj.notes
        );
    }


}
