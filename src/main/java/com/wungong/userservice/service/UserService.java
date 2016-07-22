package com.wungong.userservice.service;

import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;

import com.wungong.userservice.model.UserEntity;
import com.wungong.userservice.model.request.CreateUserRequest;
import com.wungong.userservice.model.request.UpdateUserRequest;
import com.wungong.userservice.persistence.UserRepository;
import com.wungong.userservice.utils.UserServiceUtils;

public class UserService {
	
	private final Logger log = LoggerFactory.getLogger(this.getClass());
	
	@Autowired
	UserRepository userRepository;
	
	@Autowired
	private UserServiceUtils utils;

	public UserEntity getUser(String id) {
		return userRepository.userOfId(UUID.fromString(id));
	}

	public void createUser(CreateUserRequest request) {
		UUID userId = userRepository.userId();
		userRepository.add(utils.convertToJob(userId, request));
	}

	public void deleteUser(String id) {
		UserEntity userEntity = userRepository.userOfId(UUID.fromString(id));
		userRepository.remove(userEntity);
	}

	public void updateJob(UpdateUserRequest request) {
		UUID jobId = UUID.fromString(request.getUserId());
		UserEntity jobToUpdate = userRepository.userOfId(jobId);
		userRepository.add(utils.updateUser(jobToUpdate, request));
		log.info("updated job with jobId " + jobId);
	}

}
