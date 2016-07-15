package com.wungong.userservice.model;

import java.util.UUID;

public class UserEntity {

	protected UUID id;

	public UserEntity(UUID id) {
		this.id = id;
	}

	public UUID getId() {
		return id;
	}

	public void setId(UUID id) {
		this.id = id;
	}
	
}
