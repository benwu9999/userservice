package com.wungong.userservice.controller;

import javax.ws.rs.core.Response;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.wungong.userservice.model.CreateUserResponse;
import com.wungong.userservice.model.UserEntity;
import com.wungong.userservice.model.request.CreateUserRequest;
import com.wungong.userservice.model.request.UpdateUserRequest;
import com.wungong.userservice.model.response.DeleteUserResponse;
import com.wungong.userservice.model.response.GetUserResponse;
import com.wungong.userservice.model.response.UpdateUserResponse;
import com.wungong.userservice.service.UserService;

@RestController
@RequestMapping("/job")
public class UserserviceController {
	
	@Autowired
	UserService userService;
	
	@RequestMapping(method = RequestMethod.POST, consumes="application/json", produces="application/json")
    public CreateUserResponse createJob(CreateUserRequest request) {
		userService.createUser(request);
		return new CreateUserResponse(Response.Status.CREATED);
    }
	
	@RequestMapping(method = RequestMethod.DELETE, params="id", produces="application/json")
	public DeleteUserResponse deleteJob(@RequestParam("id") String id) {
		userService.deleteUser(id);
		return new DeleteUserResponse(Response.Status.OK);
    }
	
	@RequestMapping(method = RequestMethod.PUT, consumes="application/json", produces="application/json")
    public UpdateUserResponse updateJob(UpdateUserRequest request) {
		userService.updateJob(request);
		return new UpdateUserResponse(Response.Status.OK);
    }
	
	@RequestMapping(method = RequestMethod.GET, params="id", produces="application/json")
    public GetUserResponse getUser(@RequestParam("id") String id) {
		UserEntity user = userService.getUser(id);
		return new GetUserResponse(Response.Status.OK, user);
    }
}
