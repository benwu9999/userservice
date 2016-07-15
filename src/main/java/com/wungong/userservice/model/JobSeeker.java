package com.wungong.userservice.model;

import java.util.Set;
import java.util.UUID;

import com.datastax.driver.mapping.annotations.Table;

@Table(keyspace = "userservice", name = "jobseekers")
public class JobSeeker extends UserEntity {
	
	private PersonName name;
	private Set<UUID> skillIds;
	private UUID locationID;
	private Set<PhoneNumber> phoneNumbers; 
	private Set<Email> emails;
	
	public JobSeeker(UUID id, PersonName name, Set<UUID> skillIds, 
			UUID locationID, Set<PhoneNumber> phoneNumbers, Set<Email> emails) {
		super(id);
		this.name = name;
		this.skillIds = skillIds;
		this.locationID = locationID;
		this.phoneNumbers = phoneNumbers;
		this.emails = emails;
	}

	public PersonName getName() {
		return name;
	}

	public void setName(PersonName name) {
		this.name = name;
	}

	public Set<UUID> getSkillIds() {
		return skillIds;
	}

	public void setSkillIds(Set<UUID> skillIds) {
		this.skillIds = skillIds;
	}

	public UUID getLocationID() {
		return locationID;
	}

	public void setLocationID(UUID locationID) {
		this.locationID = locationID;
	}

	public Set<PhoneNumber> getPhoneNumbers() {
		return phoneNumbers;
	}

	public void setPhoneNumbers(Set<PhoneNumber> phoneNumbers) {
		this.phoneNumbers = phoneNumbers;
	}

	public Set<Email> getEmails() {
		return emails;
	}

	public void setEmails(Set<Email> emails) {
		this.emails = emails;
	}
}
