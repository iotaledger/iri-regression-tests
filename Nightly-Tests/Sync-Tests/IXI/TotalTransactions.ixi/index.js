var System = java.lang.System;

var iri = com.iota.iri;
var Callable = iri.service.CallableRequest;
var Response = iri.service.dto.IXIResponse;
var ErrorResponse = iri.service.dto.ErrorResponse;

var tangle = IOTA.tangle;



function getTotalTransactions(){
    var count = tangle.getCount(com.iota.iri.model.persistables.Transaction.class)

    return Response.create({
        total: count
    });
}




API.put("getTotalTransactions", new Callable({ call: getTotalTransactions }))

