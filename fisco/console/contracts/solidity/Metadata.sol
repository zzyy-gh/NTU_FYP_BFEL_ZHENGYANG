pragma solidity ^0.4.6;

contract Metadata {

  mapping(string => mapping(uint256 => bytes32)) private cids;
  
  function insertCid(
    string uid, 
    uint256 round,
    bytes32 cid) 
    public
  {

    cids[uid][round]=cid;

  }
  
  function getCid(string uid, uint256 round)
    public 
    constant
    returns(bytes32 cid)
  {
    return(
      cids[uid][round]);
  } 


}
