#include "Superhero.h"
#include <iostream>
#include <string>

Superhero::Superhero(){
}

Superhero::Superhero(std::string* first, std::string* last, std::string* hero){
  this->firstName = new std::string(*first);
  this->lastName = new std::string(*last);
  this->heroName = new std::string(*hero);
}

std::string Superhero::getHeroName(){
  std::string hero = *(this->heroName);
  return hero;
}

Superhero::Superhero(const Superhero& s){
  this->firstName = new std::string(*(s.firstName));
  this->lastName = new std::string(*(s.lastName));
  this->heroName = new std::string(*(s.heroName));
}

Superhero::~Superhero(){
  delete(this->firstName);
  delete(this->lastName);
  delete(this->heroName);
}

Superhero& Superhero::operator=(const Superhero& s){
 delete(this->firstName);
 delete(this->lastName);
 delete(this->heroName);
 this->firstName = new std::string(*s.firstName);
 this->lastName = new std::string(*s.lastName);
 this->heroName = new std::string(*s.heroName);
 return *this;
}

bool Superhero::operator==(const Superhero& s) const{
  return ((*(this->firstName) == *s.firstName) && (*(this->lastName) == *s.lastName) && (*(this->heroName) == *s.heroName));
}

std::ostream& operator<<(std::ostream& os, const Superhero& s){
  os << s.firstName << ", " << s.lastName << ": " << s.heroName;
  return os;
}

bool Superhero::operator<(const Superhero& s){
  if((*(this->lastName) < *s.lastName)){
	  return true;
  }else if(*(this->lastName) > *s.lastName){
	  return false;
  }else if(*(this->lastName) == *s.lastName){
	  if(*(this->firstName) < *s.firstName){
		return true;
	  }else{
		return false;
	  }
  }
}
