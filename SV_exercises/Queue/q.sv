module Queue;

  // Exercise:

  // 1. Create a SV queue.
  int queue[$];

  // 2. Initialize the queue with {1,2,3,4}
  initial begin
    queue = {1, 2, 3, 4};

    // 3. Push front one value.
    queue.push_front(0);

    // 4. Push back one value.
    queue.push_back(5);

    // 5. Print all values.
    foreach (queue[i])
      $display(queue[i]);
	queue.delete(); 
  end

endmodule