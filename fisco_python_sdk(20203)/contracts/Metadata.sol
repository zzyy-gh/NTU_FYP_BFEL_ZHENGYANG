pragma solidity ^0.4.6;


contract Metadata {

  mapping(string => mapping(uint256 => string)) private cids;
  
  function insertCid(
    string uid, 
    uint256 round,
    string cid) 
    public
  {

    cids[uid][round]=cid;

  }
  
  function getCid(string uid, uint256 round)
    returns(string cid)
  {
    return(
      cids[uid][round]);
  } 

}

