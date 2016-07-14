package com.wungong.userservice.model;

import java.util.Collection;
import java.util.UUID;

import com.datastax.driver.mapping.annotations.UDT;

@UDT(keyspace = "userservice", name = "user")
public class User {
	
	private Name name;
	private Collection<UUID> skillIds;
	

}
