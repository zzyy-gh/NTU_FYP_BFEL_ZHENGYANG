pragma solidity ^0.4.24;

contract UserCrud {

  struct UserStruct {
    bytes32 userEmail;
    uint userAge;
    uint index;
  }
  
  mapping(string => string) private userStructs;
  address[] private userIndex;

  function insertUser(
    address userAddress, 
    bytes32 userEmail, 
    uint    userAge) 
    public
    returns(uint index)
  {
    if(isUser(userAddress)) throw; 
    userStructs[userAddress].userEmail = userEmail;
    userStructs[userAddress].userAge   = userAge;
    userStructs[userAddress].index     = userIndex.push(userAddress)-1;
    LogNewUser(
        userAddress, 
        userStructs[userAddress].index, 
        userEmail, 
        userAge);
    return userIndex.length-1;
  }
  
  function getUser(address userAddress)
    public 
    constant
    returns(bytes32 userEmail, uint userAge, uint index)
  {
    if(!isUser(userAddress)) throw; 
    return(
      userStructs[userAddress].userEmail, 
      userStructs[userAddress].userAge, 
      userStructs[userAddress].index);
  } 

}
